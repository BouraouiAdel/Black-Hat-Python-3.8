#!/usr/bin/python3.8

import argparse
import textwrap

parser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter, epilog =textwrap.dedent("""\
					Examples:
					bhpnet.py -t 192.168.0.1 5555 -l -c
					bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe
					bhpnet.py -t 192.168.0.1 -p 5555 -l -e = "cat /etc/passwd"
					echo \"ABCDEFGHI\" | ./bhpnet.py -t 192.168.11.12 -p 135"""))
parser.add_argument("-l", "--listen", help = "Listen on [host]:[port] for incoming connections.")
parser.add_argument("-e", "--execute", metavar = "File_to_run", help = "Execute the given file upon receiving a connection.")
parser.add_argument("-c", "--commandshell", help = "Initialize a command shell.")
parser.add_argument("-u", "--upload", metavar = "Destination", help = "Upon receiving connection upload a file and write to [destination]")

args = parser.parse_args()
