class Spam():
	def __init__(self, chat_id, spam_max_count):
		self.chat_id = chat_id
		self.spam_list = []
		self.last_usr_id = 0
		self.spam_count = 0
		self.spam_max_count = spam_max_count
		self.last_txt = ""

	def tick(self, usr_id, msg, txt):
		if usr_id == self.last_usr_id and txt == self.last_txt: 
			self.spam_count += 1
			self.spam_list.append(msg)
		else: 
			self.spam_count = 0
			self.spam_list = []

		self.last_usr_id = usr_id
		self.last_txt = txt
		
		if self.spam_count >= self.spam_max_count:
			return_list = [self.spam_list, self.spam_count]
			self.spam_count = 0
			self.spam_list = []
			self.last_usr_id = 0
		else:
			return_list = [-1]

		return return_list




