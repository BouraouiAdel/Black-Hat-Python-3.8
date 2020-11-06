import argparse
import threading
import sys
import socket

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		server_socket.bind((local_host, local_port))
	except:
		print("[!!] Failed to listen on %s:%d." % (local_host, local_port))
		print("[!!] Check for other listening socket or correct permissions.")
		sys.exit(0)

	print("[*] Listening on %s:%d" % (local_host, local_port))

	server_socket.listen(5)

	while True:
		(client_socket, addr) = server_socket.accept()

		print("[==>] Received incoming connection from %s:%d" % (addr[0], addr[1]))

		# Start a thread to talk to the remote host.
		proxy_thread = threading.Thread(target = proxy_handler, args = (client_socket, remote_host, remote_port, receive_first))
		proxy_thread.start()

def proxy_handler(client_socket, remote_host, remote_port, receive_first):

	# Connect to the remote host
	remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	remote_socket.connect((remote_host, remote_port))

	# Receive data from the remote end/host if necessary.
	if receive_first:

		remote_buffer = receive_from(remote_socket)
		hexdump(remote_buffer)

		# Send it to our response handler
		remote_buffer = response_handler(remote_buffer)

		# If we have data to send to our local client, send it
		if len(remote_buffer):
			print("[<==] Sending %d bytes to localhost." % len(remote_buffer))
			client_socket.send(remote_buffer)

	# Now, let's loop : read from local, send to remote and read from remote, send to local.

	while True:

		# Read from local host.
		local_buffer = receive_from(client_socket)

		if len(local_buffer):

			print("[==>] Received %d bytes from localhost." % len(local_buffer))
			hexdump(local_buffer)

			# Send it to our request handler.
			local_buffer = request_handler(local_buffer)

			# Send off the data to the remote host.
			remote_socket.send(local_buffer)
			print("[==>] Sent to remote.")

			# Receive back the reponse.
			remote_buffer = receive_from(remote_socket)

		if len(remote_buffer):

			print("[<==] Received %d bytes from remote." % len(remote_buffer))
			hexdump(remote_buffer)

			# Send to our response handler
			remote_buffer = response_handler(remote_buffer)

			# Send the response to the local socket
			client_socket.send(remote_buffer)

			print("[<==] Sent to localhost.")

		# If no more data on either side, close the connections.
		if not len(local_buffer) or not len(remote_buffer):
			client_socket.close()
			remote_socket.close()
			print("[*] No more data. Closing connections.")

			break

def receive_from(target_socket):

	received_data = b""

	# We set a 2 second timeout; depending on
	# your target, this may need to be adjusted.

	target_socket.settimeout(5)

	try:
		# Keep reading into the buffer until
		# there's no more data or we time out.
		while True:
			received_packet = target_socket.recv(1024)
			length_received_packet = len(received_packet)
			received_data += received_packet

			if lenght_received_packet < 1024:
				break
	except:
		target_address = target_socket.getpeername()[0]
		print("[!!] Time out ! Failed to listen on the target %s" % (target_address))

	return received_data

# Print the hexadecimal dump of the given bytestring
def hexdump(data_source, length = 16):

	result_buffer = []
	# We are assuming here that the exchanged text is encoded in UTF-8.
	for i in range(0, len(data_source), length):
		bytes_buffer = data_source[i:i+length]
		bytes_column = b" ".join(["%02X".encode(encoding = "UTF-8") % byte_element\
					 	for byte_element in bytes_buffer]) # Hexadecimal representation.
		text_column = b"".join([bytes([byte_element]) if 0x20 <= byte_element < 0x7F else b'.'\
			 			for byte_element in bytes_buffer]) # Text representation.
		result_buffer.append(b"%04X   %-*s   %s" % (i, length * 3, bytes_column, text_column))
								# the number 3 is here for 2 hexadecimal symbols a 1 space character.

	print(b"\n".join(result_buffer).decode(encoding = "UTF-8"))

# Modify any requests destined for the remote host.
def request_handler(request_buffer):
	# Perform packet modifications.

	return request_buffer

# Modify any responses destined for the local host
def response_handler(response_buffer):
	# Perform packet modification

	return response_buffer

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description = "A simple TCP proxy.")

	parser.add_argument("local_host", help = "The local address of the proxy.")
	parser.add_argument("local_port", type = int, help = "The port that is going to be used for the proxy.")
	parser.add_argument("remote_host", help = "The remote host's address with which we are going to interact.")
	parser.add_argument("remote_port", type = int, help = "The remote host's port with which we are going to interact.")
	parser.add_argument("-rf", "--receive_first", action = "store_true", help = "Determine if the proxy will have to send a message first or not.")

	args = parser.parse_args()

	server_loop(args.local_host, args.local_port, args.remote_host, args.remote_port, args.receive_first)
