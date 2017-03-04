import sys,os
from socket import *
from Queue import Queue
from threading import Thread
from commands import Commands



threads=[]
activE=True
threadLimit=100
numb_of_threads=0


hostname=sys.argv[1]
port_number=int(sys.argv[2])
sock=socket(AF_INET,SOCK_STREAM)
sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
sock.bind((hostname,port_number))
sock.listen(10)

def messages(connect):
	while activE:
		msg=connect.recv(2048)
		if msg[:2] == "cd":
		
		elif msg=="ls":
			
		elif msg[:4] =="read":
				
		elif msg[:5] =="write":
			
		elif msg[:4]=="HELO":
				print "HELO Received: "+msg
				msg="%sIP:%s\nPort:%s\nStudentID:13319829\n"%(msg,str(gethostbyname(gethostname())),int(sys.argv[2]))
				connect.sendall(msg)
				print "HELO Sent"
		elif msg[:12]=="KILL_SERVICE":				
				os._exit(1)
				activE=False
		else:
			errmsg="ERROR_CODE:1\nERROR_DESCRIPTION: Parse error\n"
			connect.sendall(errmsg)
		


while activE:
	if numb_of_threads<threadLimit:
		connect,address=sock.accept()
		threads.append(Thread(target=messages,args=(connect,)))		
		threads[numb_of_threads].start()
		global numb_of_threads
		numb_of_threads=numb_of_threads+1
	else:
		print("max threads reached")

