import sys,os
from socket import *
from Queue import Queue
from threading import Thread
import collections
from chat_room import ChatRoom

chat_room=ChatRoom(sys.argv[1],int(sys.argv[2]))
rooms=collections.OrderedDict()
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
		if msg[:13] == "JOIN_CHATROOM":
			print("joining chatroom")
			msgs=msg.split("\n")
			chatroom=msgs[0].split(":")[1]
			client_name=msgs[3].split(":")[1]
			numb=0
			for c in chatroom:
				numb=numb+ord(c)
			room_ref=numb%10
			number=0
			for c in client_name:
				number=number+ord(c)
			join_id=number%10
			chat_room.joinroom(rooms,chatroom,client_name,room_ref,join_id,connect)
			#retmsg="JOINED_CHATROOM:%s\nSERVER_IP:%s\nPORT:%s\nROOM_REF:%s\nJOIN_ID:%s\n"%(chatroom,sys.argv[1],int(sys.argv[2]),room_ref,join_id)
			#connect.sendall(retmsg)
			print("joined chatroom")
		elif msg[:14] =="LEAVE_CHATROOM":
			print("leaving chatroom")
			msgs=msg.split("\n")
			room_ref=int(msgs[0].split(":")[1])
			join_id=int(msgs[1].split(":")[1])
			client_name=msgs[2].split(":")[1]
			chat_room.leaveroom(rooms,room_ref,join_id,client_name,connect)
			#retmsg="LEFT_CHATROOM:%s\nJOIN_ID:%s\n"%(str(room_ref),str(join_id))
			#connect.sendall(retmsg)
			print("left chatroom")
		elif msg[:10] =="DISCONNECT":
			print("client disconnecting")
			msgs=msg.split("\n")
			client_name=msgs[2].split(":")[1]
			number=0
			for c in client_name:
				number=number+ord(c)
			join_id=number%10
			chat_room.disconnect(rooms,join_id,client_name,connect,activE)
			#retmsg="DISCONNECT: 0\nPORT: 0\nCLIENT_NAME: Name\n"
			#connect.sendall(retmsg)
			print("client disconnected")	
		elif msg[:4] =="CHAT":
			print("received message")
			msgs=msg.split("\n")
			room_ref=int(msgs[0].split(":")[1])
			join_id=int(msgs[1].split(":")[1])
			client_name=msgs[2].split(":")[1]
			data=msgs[3].split(":")[1]
			chat_room.chat(rooms,room_ref,join_id,client_name,data,connect)	
			#retmsg="CHAT:%s\nCLIENT_NAME:%s\nMESSAGE:%s\n\n"%(str(room_ref),str(client_name),data)
			#connect.sendall(retmsg)
			print("message received")
		elif msg[:4]=="HELO":
				print "HELO Received: "+msg
				msg="%sIP:%s\nPort:%s\nStudentID:13319829\n"%(msg,str(gethostbyname(gethostname())),int(sys.argv[2]))
				connect.sendall(msg)
				print "HELO Sent"
		elif msg[:12]=="KILL_SERVICE":				
				os._exit(1)
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
#if __name__ == "__main__":
#	chat_server(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
