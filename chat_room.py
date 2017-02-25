def broadcast(msg,connect,chatrooms,room_ref,join_id):
	for join_id,connect in chatrooms[room_ref].iteritems():
		connect.sendall(msg)


class ChatRoom:

	def __init__(self,hostname,portnum):
		self.hostname=hostname
		self.portnum=portnum
		
	def joinroom(self,chatrooms,roomname,clientname,roomref,join_id,connect):
		if roomref not in chatrooms:			
			chatrooms[roomref]={}
		if join_id not in chatrooms[roomref]:
			chatrooms[roomref][join_id]=connect
			retmsg="JOINED_CHATROOM:%s\nSERVER_IP:%s\nPORT:%s\nROOM_REF:%s\nJOIN_ID:%s\n"%(roomname,self.hostname,self.portnum,roomref,join_id)
			connect.sendall(retmsg)
			broadmsg="CHAT:%s\nCLIENT_NAME:%s\nMESSAGE:%s has joined the chat\n\n"%(str(roomref),str(clientname),str(clientname))
			broadcast(broadmsg,connect,chatrooms,roomref,join_id)
	
	def leaveroom(self,chatrooms,room_ref,join_id,clientname,connect):
	
		retmsg="LEFT_CHATROOM:%s\nJOIN_ID:%s\n"%(str(room_ref),str(join_id))
		connect.sendall(retmsg)
		broadmsg="CHAT:%s\nCLIENT_NAME:%s\nMESSAGE:%s has left the chat\n\n"%(str(room_ref),str(clientname),str(clientname))
		broadcast(broadmsg,connect,chatrooms,room_ref,join_id)
		del chatrooms[room_ref][join_id]
	
	def disconnect(self,chatrooms,join_id,clientname,connect,active):
		for room_ref in chatrooms.keys():
			if join_id in chatrooms[room_ref]:
				#retmsg="DISCONNECT: 0\nPORT: 0\nCLIENT_NAME: Name\n"
				#connect.sendall(retmsg)
				broadmsg="CHAT:%s\nCLIENT_NAME:%s\nMESSAGE:%s has disconnected from the chat\n\n"%(str(room_ref),str(clientname),str(clientname))
				broadcast(broadmsg,connect,chatrooms,room_ref,join_id)
				del chatrooms[room_ref][join_id]
		active=False
	def chat(self,chatrooms,room_ref,join_id,clientname,msg,connect):
		broadmsg="CHAT:%s\nCLIENT_NAME:%s\nMESSAGE:%s\n\n"%(str(room_ref),str(clientname),msg)
		broadcast(broadmsg,connect,chatrooms,room_ref,join_id)
