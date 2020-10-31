#!/usr/bin/python3.8

import socket

target_host = "127.0.0.1"
target_port = 5555

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Send some data
client.sendto(b"AAABBBCCC", (target_host, target_port))
# Receive some data
(bytes, address) = client.recvfrom(4096)

print(bytes.decode(encoding="UTF-8"))

