#!/usr/bin/python3.8

import socket

target_host = "www.google.com"
target_port = 80

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect (Three-way handshake: SYN->SYN-ACK->ACK) to the client
client.connect((target_host, target_port))
# Send some data
client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")
# Receive some data
response = client.recv(4096)

print(response.decode(encoding = "UTF-8"))
