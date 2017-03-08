import os
import socket
import threadpool
import servermanager

pool=threadpool.ThreadPool(1000)

port_number=8080

address=socket.gethostbyname(socket.gethostname())

manager=servermanager.ServerManager("root")

activE=True

def run_server():
	sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server_address=('0.0.0.0',port_number)
	sock.bind(server_address)
	sock.listen(1)
	
	while activE:
		connect,user_address=sock.accept()
		pool.add_task(
			messages,
			connect,
			user_address
		)

#Add in locking and caching
def messages(connect,user_address):
	try:
		user_id=manager.add_user(connect)
		msg=connect.recv(2048)
		data_in_msg=msg.split("////")
		if data_in_msg[0] == "cd":
			manager.change(data_in_msg[1],user_id)
		elif data_in_msg[0] == "cd ..":
			manager.changeup(user_id)
		elif msg=="ls":
			manager.list_all(user_id)
		elif data_in_msg[0] =="mkdir":
			manager.make(data_in_msg[1],user_id)
		elif data_in_msg[0] =="rmdir":
			manager.remove(data_in_msg[1],user_id)
		elif data_in_msg[0] =="read":
			manager.read_file(data_in_msg[1],user_id)
		elif data_in_msg[0] =="write":
			manager.write_to_file(data_in_msg[1],data_in_msg[2],user_id)
		elif data_in_msg[0] =="delete":
			manager.delete_file(data_in_msg[1],user_id)
		elif data_in_msg[0] =="exit":
			manager.disconnect_user(connect,user_id)
		elif msg=="KILL_SERVICE":				
			connection.close()
			os._exit(0)
		else:
			errmsg="ERROR\n"
			connect.sendall(errmsg)
	except:	
		errmsg="ERROR\n"
		connect.sendall(errmsg)
		connect.close()
		
if __name__ == '__main__':
    run_server()
    pool.wait_completion()