from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class User(object):
	def __init__(self, id):
		self.id = id
		self.friends = set()
		self.purchases = []

	def add_friend(self, id):
		self.friends.add(id)

	def remove_friend(self, id):
		self.friends.remove(id)

	def add_purchase(self, amount, timestamp):
		# TODO: improve memory usage of this
		self.purchases.append((timestamp, amount))


class SocialNetwork(object):
	def __init__(self):
		# id -> user object map
		self.users = {}

	def add_user(self, id):
		if id in self.users:
			return
		
		self.users[id] = User(id)

	def update_friend(self, id1, id2, befriend):
		self.add_user(id1)
		self.add_user(id2)

		if befriend:
			self.users[id1].add_friend(id2)
			self.users[id2].add_friend(id1)
		else:
			self.users[id1].remove_friend(id2)
			self.users[id2].remove_friend(id1)

	def add_purchase(self, id, amount, timestamp):
		current_user = self.users[id]
		current_user.add_purchase(amount, timestamp)		

	def get_tracked_purchase(self, id, degree, num_tracked):
		users_in_degree = set([id])
		boundary = set([id])
		# get all users within the social network of `id` defined by `degree`
		for i in range(degree):
			new_boundary = set()
			for bid in boundary:
				bid_user = self.users[bid]
				for fid in bid_user.friends:
					if fid in users_in_degree:
						continue
	
					users_in_degree.add(fid)
					new_boundary.add(fid)

			boundary = new_boundary

		users_in_degree.remove(id)

		# get the lastest `num_tracked` purchases
		# TODO: improve the speed of this
		all_purchases = []
		for uid in users_in_degree:
			all_purchases.extend(self.users[uid].purchases)

		all_purchases.sort()

		return [t[1] for t in all_purchases[-num_tracked:]]





