

class User:
	def __init__(self, id, socket, path_root):
		self.id=id
		self.socket=socket
		self.dir_level=0
		self.dir_path=[path_root]

	def change_directory(self, dir_name ):
		self.dir_level=self.dir_level + 1
		self.dir_path.append( dir_name )

	def move_up_directory(self):
		if self.dir_level > 0:
			self.dir_path.pop()
			self.dir_level=self.dir_level - 1
			return 0
		else:
			return 1


#Add in locking and caching
#create event tracker
#add more error handling
class ServerManager:
	
	current_users=[]
	
	next_user_id=0
	
	def __init__(self,root_path):
		self.root_path=root_path
		
	def create_user_id(self):
		result=self.next_user_id
		self.next_user_id=self.next_user_id+1
		return result
		
	def add_user(self, connection):
		new_user_id=self.create_user_id()
		new_user=User(new_user_id, connection, self.root_path)
		self.current_users.append(new_user)
		return new_user_id
		
	def remove_user(self, user):
		x=0
		for user in self.current_users:
			if user.id == user.id:
				self.current_users.pop(x)
			x=x + 1

	def get_active_user(self, user_id):
		for user in self.current_users:
			if user.id == user_id:
				return user

	def update_user(self, user):
		x=0
		for user in self.current_users:
			if user.id == user.id:
				self.current_users[x]=user
			x=x + 1

	def disconnect_user(connect, user_id):
		user=self.get_active_user(user_id)
		self.remove_user(user)
		connect.close()
	
	def list_all(self,user_id):
		blank=""
		path=self.getcurrentpath(user_id,blank)
		list_of_items=os.listdir(path)
		result=""
		for item in list_of_items:
			result=result +item + "\n"
		return result
		
	def change(self,data_in_msg,user_id)	:
		user=self.get_active_user(user_id)
		user.change_directory(data_in_msg)
		self.update_user(user)
		
	def changeup(self,user_id):
		user=self.get_active_user(user_id)
		user.move_up_directory()
		self.update_user(user)
		
	def make(self,data_in_msg,user_id):
		path=self.getcurrentpath(user_id,data_in_msg)
		os.makedirs(path)
		
	def remove(self,data_in_msg,user_id):
		path=self.getcurrentpath(user_id,data_in_msg)
		shutil.rmtree(path)
		
	def read_file(self,data_in_msg,user_id):
		path=self.getcurrentpath(user_id,data_in_msg)
		file=open(path, 'r')
		file_contents=file.read()
	
	def write_to_file(self,data_in_msg,data_in_msg_2,user_id):
		path=self.getcurrentpath(user_id,data_in_msg)
		file=open(file_path, 'w+')
		file.truncate()
		file.write(data_in_msg_2)
		
	def delete_file(self,data_in_msg,user_id):
		path=self.getcurrentpath(user_id,data_in_msg)
		os.remove(path)	
	
	def getcurrentpath(self,user_id,name):
		user=self.get_active_user(user_id)
		path=""
		for level in user.dir_path:
			path=path + "%s/" % level
		path=path+name
		return path