import threading
import paramiko
import subprocess

def ssh_command(ip, username, password, command):

	client = paramiko.SSHClient()
	# client.load_host_keys("/home/john/Documents/Black-Hat-Python-3.8/Chap2")
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(ip, username = username, password = password)
	ssh_session = client.get_transport().open_session()

	if ssh_session.active:
		ssh_session.exec_command(command)
		print(ssh_session.recv(1024))
if __name__ == "__main__":

	ssh_command("127.0.0.1", "justin", "lovesthepython", "id")
