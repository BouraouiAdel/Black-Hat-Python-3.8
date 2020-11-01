#!/usr/bin/python3.8

import argparse
import textwrap
import sys
import subprocess

parser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter, epilog =textwrap.dedent("""\
					Examples:
					bhpnet.py -t 192.168.0.1 5555 -l -c
					bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe
					bhpnet.py -t 192.168.0.1 -p 5555 -l -e = "cat /etc/passwd"
					echo "ABCDEFGHI" | ./bhpnet.py -t 192.168.11.12 -p 135
					"""))
parser.add_argument("-t", "--target", default = "0.0.0.0", help ="The IPv4 address of the target host machine")
parser.add_argument("-p", "--port", type = int, help = "The port number that is going to be used to communicate with the target host machine")
parser.add_argument("-l", "--listen", action = "store_true",\
			help = "Listen on [host]:[port] for incoming connections.")
parser.add_argument("-e", "--execute", help = "Execute the given file upon receiving a connection.")
parser.add_argument("-c", "--commandshell", action = "store_true",\
			help = "Initialize a command shell.")
parser.add_argument("-u", "--upload", help = "Upon receiving connection upload a file and write to [destination]")

args = parser.parse_args()

# This part verifies that key arguments (the target IP and the port) are given and correct.

# TODO: A way to verify that the given IP respects the IPv4 format. Example: A function that does it by using regex.
elif args.port == 0:
	parser.error("For TCP, the port number 0 is reserved and cannot be used.")
elif args.port < 1 or args.port > 65535:
	parser.error("For TCP, the usable port numbers range from 1 to 65535.")

# Send off data from the standard input.
if not listen and target != "0.0.0.0":
	"""
	The file object stdin enables to read multiple command lines at once.
	In order to quit, the "CTRL-D" button must be pressed.
	"""

	input_command_lines = sys.stdin.read()

	# To send data off.
	client_sender(args.target, args.port, input_command_lines)

# Listen to connections and will potentially upload things,
# execute commands and drop a shell back depending on our command
# line options above.
if listen:
	server_loop(args.target)

def client_sender(target_address, target_port, data_to_send):

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		# Connection to the target host.
		client_socket.connect((target_address, target_port))

		if data_to_send:
			client_socket.send(data_to_send)

		# Here, we continously receive and send off data to the remote target until the user kills the script.
		while True:
			response = ""

			while True:
				received_data = client.recv(1024)
				received_data_length = len(received_data)
				response += received_data

				if received_data_length < 1024:
					break

			print(response.decode(encoding = "UTF-8"))

			data_to_send = sys.stdin.read()
			client_socket.send(data_to_send)

	except:
		print("[*] Exception! Exiting.")

		# Close the connection.
		client_socket.close()

def server_loop(target, port, upload, execute, command):

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((target, port))
	server.listen(5)

	while True:
		(client_socket, address) = server.accept()

		client_thread = threading.Thread(target = client_handler, args = (client_socket, upload, execute, command))

def run_command(command):

	command = command.rstrip() 	# The Newline character and the whitespace character
					# are stripped from the end of the string.

	# The given command is run in a subprocess to easily get
	# the stdout and the stderr.
	try:
		output = subprocess.check_output(command, stderr = subprocess.STDOUT, shell = True)
		# Here, the stdout and the stderr are merged together by "stderr = subprocess.STDOUT".
		# Moreover, the command will be a string. That's why, the keyword argument "shell" must be set on True.
	except:
		output = "Failed to execute the command.\r\n"

	return output
