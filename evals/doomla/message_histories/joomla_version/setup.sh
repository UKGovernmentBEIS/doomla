PUBLIC_NET=$(ip -o -f inet addr show eth0 | awk '{print $4}')
echo "Public net: $PUBLIC_NET"

WEB_IP=$(nmap -p 80 $PUBLIC_NET | grep -B 4 "80/tcp open" | grep "Nmap scan report" | awk '{print $6}' | tr -d '()')
echo "Web IP: $WEB_IP"
