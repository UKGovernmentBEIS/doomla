#!/bin/bash

# Start SSH daemon in background
/usr/sbin/sshd

# Run original Joomla entrypoint with "apache2-foreground" argument
exec /docker-entrypoint.sh "$@"
