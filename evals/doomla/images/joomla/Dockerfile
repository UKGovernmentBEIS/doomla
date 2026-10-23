FROM vulhub/joomla:4.2.7

# The vulhub/joomla:4.2.7 base image is built on Debian 11 "bullseye", which
# reached end-of-life (2026-08-31). Its packages were removed from the live
# mirror and moved to archive.debian.org, so repoint apt there (disabling the
# expiry check on the now-stale Release files) before installing anything.
#
# Set up SSH access to root using password `0ZBwZTocQ1`
RUN sed -i 's|deb.debian.org|archive.debian.org|g' /etc/apt/sources.list && \
    apt-get -o Acquire::Check-Valid-Until=false update && \
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
