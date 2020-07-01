#!/usr/bin/python3.8

import socket
import threading

bind_ip = "127.0.0.1"
bind_port = 5555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((bind_ip, bind_port))
server_socket.listen(5)

print("[*] Listening on %s:%d" % (bind_ip, bind_port))

# This is our client-handling thread
def handle_client(client_socket):

	# Print out what the client sends
	request = client_socket.recv(1024).decode(encoding = "UTF-8")

	print("[*] Received: %s" % request)

	# Send back a packet
	client_socket.send(b"ACK!")

	client_socket.close()

while True:

	(client_socket, addr) = server_socket.accept()

	print("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))

	# Spin up our client thread to handle incoming data
	client_handler = threading.Thread(target = handle_client, args = (client_socket,))
	client_handler.start()
