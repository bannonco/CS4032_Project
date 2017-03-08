import socket
import threadpool
import time
import os

pool=threadpool.ThreadPool(10)

port_number = 8080

address = socket.gethostbyname(socket.gethostname())

activE=True


def server_connect():
	sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server_address=('0.0.0.0',port_number)
	sock.connect(server_address)
	
	while activE:
		input=raw_input()
		message=create_message(input)
		sock.send(message)
		if message=="exit":
			os._exit(0)

			
#Add in locking and caching
def create_message(input):
	split_input = input.split(" ")
	if split_input[0] == "write":
		try:
			file = open(split_input[1])
			file_contents = file.read()
			return "%s////%s////%s" % (split_input[0], split_input[1], file_contents)
		except IOError:
			print "no such file in source directory"
			return ""
	else:
		return '////'.join(split_input)
	
if __name__ == '__main__':
	server_connect()
	pool.wait_completion()