FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y \
    openssh-server \
    sudo && \
    rm -rf /var/lib/apt/lists/*

# Create a user 'melo' with a hard-to-guess password
RUN useradd -m -s /bin/bash melo && \
    echo 'melo:QWxVgZ16Rw' | chpasswd

# Allow 'melo' to use sudo without a password
RUN echo 'melo ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/melo

# Set up SSH key-based authentication for melo
RUN mkdir -p /home/melo/.ssh
COPY authorized_keys /home/melo/.ssh/
RUN chown -R melo:melo /home/melo/.ssh && \
    chmod 700 /home/melo/.ssh && \
    chmod 600 /home/melo/.ssh/authorized_keys

# Create directory for SSH daemon
RUN mkdir -p /var/run/sshd

# Expose the SSH port
EXPOSE 22

# Start SSH daemon in the foreground
CMD ["/usr/sbin/sshd", "-D"]
