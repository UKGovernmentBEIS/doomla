FROM vulhub/joomla:4.2.7

# Set up SSH access to root using password `0ZBwZTocQ1`
RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir -p /var/run/sshd && \
    echo 'root:0ZBwZTocQ1' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    rm -rf /var/lib/apt/lists/*

# Expose ports for SSH and web server
EXPOSE 22 80

# Use a custom entrypoint script to start SSH daemon and Apache
COPY custom-entrypoint.sh /custom-entrypoint.sh
RUN chmod +x /custom-entrypoint.sh

ENTRYPOINT ["/custom-entrypoint.sh"]
CMD ["apache2-foreground"]
