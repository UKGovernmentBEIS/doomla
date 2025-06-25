# It's recommended to use a specific version in order to ensure reproducibility.
# You can pull the latest Kali Linux release using:
# docker pull kalilinux/kali-last-release
# docker inspect -f '{{json .RepoDigests}}' kalilinux/kali-last-release | jq -r '.[0]'
FROM kalilinux/kali-last-release@sha256:396fe3b46c76cf9fd095d9ccf630fc0bac9280f8118b8afb8be1df9e8c1e75ad

# Install the  kali-linux-headless metapackage (and any other packages you'd like)
RUN apt-get update && \
    apt-get install -y \
    kali-linux-headless \
    sshpass && \
    rm -rf /var/lib/apt/lists/*

# Fix a known issue with the nmap package in Kali Linux (https://bugs.kali.org/view.php?id=9085)
RUN setcap cap_net_raw,cap_net_bind_service+eip /usr/lib/nmap/nmap

# Start the agent in the /root/ directory
WORKDIR /root/

# Keep the container running for up to 86400 seconds (1 day)
CMD [ "sleep", "86400" ]
