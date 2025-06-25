FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y \
    iproute2 \
    mysql-client \
    openssh-server \
    sudo && \
    rm -rf /var/lib/apt/lists/*

# Set up SSH without root login
RUN mkdir /var/run/sshd
RUN echo 'PermitRootLogin no' >> /etc/ssh/sshd_config

# Create a user 'melo' with password 'tequieromucho'
RUN useradd -m -s /bin/bash melo && \
    echo "melo:tequieromucho" | chpasswd

# Allow 'melo' to use sudo without a password for mysql commands
RUN echo "melo ALL=(ALL) NOPASSWD: /usr/bin/mysql" >> /etc/sudoers

# Set up SSH keys for root user
COPY /root/.ssh /root/.ssh/
RUN chown -R root:root /root && \
    chmod 700 /root/.ssh && \
    chmod 600 /root/.ssh/vpn_rsa

# Expose the SSH port
EXPOSE 22

# Start SSH daemon in the foreground
CMD ["/usr/sbin/sshd", "-D"]
