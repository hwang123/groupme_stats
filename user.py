import numpy
from matplotlib import pyplot as plt 

class User:
	"""
    A class used to represent a single user
    ...

    Attributes
    ----------
    user_id: String
        A unique user identifier
    messages: [String]
        A list of message texts
    usernames: [String]
        A list of usernames, sorted oldest first
    popular_posts: [(String, int)]
        A list of popular posts by the user (>10 likes), stored as tuple
        containing the message text and the number of likes
    likes_received: int
    	Number of total likes received
    likes_given: int
		Number of total likes given
	word_count: int
		Number of total words posted by the user
	likes: {String: int}
		
    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """
	def __init__(self, user_id):
		# String
		self.user_id = user_id

		# [String]
		self.messages = []
		self.usernames = []

		# Tuple (String text,  int num_likes)
		self.popular_posts = []

		# Int
		self.likes_received = 0
		self.likes_given = 0
		self.word_count = 0

		# Map{string:Int}
		self.likes = {}

	def get_user_id(self):
		return self.user_id

	## Username
	def add_username(self, username):
		if username not in self.usernames:
			self.usernames.append(username)

	def get_usernames(self):
		return self.usernames

	def get_most_recent_username(self):
		return self.usernames[-1]

	## Messages 
	def add_message(self, message, num_likes, timestamp):
		self.messages.append(message)
		self.increment_likes_received(num_likes)
		if num_likes > 10:
			self.popular_posts.append((message, num_likes))

	def get_messages(self):
		return self.messages

	def get_num_messages(self):
		return len(self.messages)

	def get_popular_messages(self):
		return self.popular_posts

	## Likes
	def increment_likes_given(self, user_id, num_likes=1):
		self.likes_given += num_likes

		if user_id not in self.likes:
			self.likes[user_id] = 1
		else:
			self.likes[user_id] = self.likes[user_id] + 1


	def get_likes_given(self):
		return self.likes_given

	def increment_likes_received(self, num_likes=1):
		self.likes_received += num_likes

	def get_likes_received(self):
		return self.likes_received

	def get_like_map(self):
		return self.likes

	## Plotting
