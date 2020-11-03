import argparse
import threading
import sys


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		server_socket.bind((local_host, local_port))
	except:
		print("[!!] Failed to listen on %s:%d." % (local_host, local_port)
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

parser = argparse.ArgumentParser(description = "A simple TCP proxy.")

parser.add_argument("local_host", help = "The local address of the proxy.")
parser.add_argument("local_port", type = int, help = "The port that is going to be used for the proxy.")
parser.add_argument("remote_host", help = "The remote host's address with which we are going to interact.")
parser.add_argument("remote_port", type = int, help = "The remote host's port with which we are going to interact.")
parser.add_argument("-rf", "--receive_first", action = "store_true", help = "Determine if the proxy will have to send\
										 a message first or not.")

args = parser.parse_args()

server_loop(args.local_host, args.local_port, args.remote_host, args.remote_port, args.receive_first)
