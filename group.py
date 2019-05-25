import numpy as np 
import math
from matplotlib import pyplot as plt 
from datetime import datetime

class Group:
	def __init__(self, starting_time, ending_time):
		self.starting_time = starting_time
		self.ending_time = ending_time
		self.messages = []

	def add_message(self, message, num_likes, time):
		msg = (message, num_likes, time)
		self.messages.append(msg)

	def show_historic_likes(self, num_buckets = 100, num_labels = 5):
		time_range = self.ending_time - self.starting_time
		dt = time_range / num_buckets

		ts_to_likes = [0 for i in range(num_buckets + 1)]
		total_likes = 0
		for message in self.messages:
			num_likes = message[1]
			ts = message[2]
			ts_bucket = math.floor((ts - self.starting_time)/dt)
			ts_to_likes[ts_bucket] = ts_to_likes[ts_bucket] + num_likes
			total_likes += num_likes

		print(str(total_likes) + ' total likes.')


		parsed_starting_time = datetime.utcfromtimestamp(self.starting_time).strftime('%Y-%m-%d')
		parsed_ending_time = datetime.utcfromtimestamp(self.ending_time).strftime('%Y-%m-%d')

		y_pos = np.arange(len(ts_to_likes))

		plt.bar(y_pos, ts_to_likes, align='center', alpha=0.5)
		plt.xticks([])
		plt.ylabel('Likes')
		plt.xlabel('From ' + parsed_starting_time + ' to ' + parsed_ending_time)
		plt.title('Likes over time')

		plt.show()

	def show_historic_posts(self, num_buckets = 100, num_labels = 5):
		time_range = self.ending_time - self.starting_time
		dt = time_range / num_buckets

		ts_to_posts = [0 for i in range(num_buckets + 1)]

		for message in self.messages:
			num_likes = message[1]
			ts = message[2]
			ts_bucket = math.floor((ts - self.starting_time)/dt)
			ts_to_posts[ts_bucket] = ts_to_posts[ts_bucket] + 1


		parsed_starting_time = datetime.utcfromtimestamp(self.starting_time).strftime('%Y-%m-%d')
		parsed_ending_time = datetime.utcfromtimestamp(self.ending_time).strftime('%Y-%m-%d')

		y_pos = np.arange(len(ts_to_posts))

		plt.bar(y_pos, ts_to_posts, align='center', alpha=0.5)
		plt.xticks([])
		plt.ylabel('Posts')
		plt.xlabel('From ' + parsed_starting_time + ' to ' + parsed_ending_time)
		plt.title('Posts over time')

		plt.show()

