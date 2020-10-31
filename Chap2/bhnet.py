#!/usr/bin/python3.8

import argparse
import textwrap

parser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter, epilog =textwrap.dedent("""\
					Examples:
					bhpnet.py -t 192.168.0.1 5555 -l -c
					bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe
					bhpnet.py -t 192.168.0.1 -p 5555 -l -e = "cat /etc/passwd"
					echo "ABCDEFGHI" | ./bhpnet.py -t 192.168.11.12 -p 135
					"""))
parser.add_argument("-t", "--target", help ="The IPv4 address of the target host machine")
parser.add_argument("-p", "--port", type = int, help = "The port number that is going to be used to communicate with the target host machine")
parser.add_argument("-l", "--listen", action = "store_true",\
			help = "Listen on [host]:[port] for incoming connections.")
parser.add_argument("-e", "--execute", help = "Execute the given file upon receiving a connection.")
parser.add_argument("-c", "--commandshell", action = "store_true",\
			help = "Initialize a command shell.")
parser.add_argument("-u", "--upload", help = "Upon receiving connection upload a file and write to [destination]")

args = parser.parse_args()

# This part verifies that key arguments (the target IP and the port) are given and correct.
if args.target == None:
	parser.error("A target must be specified.")
# TODO: A way to verify that the given IP respects the IPv4 format. Example: A function that does it by using regex.
elif args.port == 0:
	parser.error("For TCP, the port number 0 is reserved and cannot be used.")
elif args.port < 1 or args.port > 65535:
	parser.error("For TCP, the usable port numbers range from 1 to 65535.")
