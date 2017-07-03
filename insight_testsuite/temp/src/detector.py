from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import numpy as np

from social_network import SocialNetwork


class Detector(object):
	def __init__(self, json_lines, degree, num_tracked):
		# TODO: relax assumption, sort json_lines first by timestamp
		self.degree = degree
		self.num_tracked = num_tracked
		self.social_network = SocialNetwork()

		for ln in json_lines:
			info = json.loads(ln)
			self.process_event(info, is_init=True)

	def process_event(self, info, is_init=False):
		event_type = info['event_type']
		if (event_type in ['befriend', 'unfriend']):
			id1 = info['id1']
			id2 = info['id2']
			self.social_network.update_friend(id1, id2, event_type == 'befriend')
			return None

		elif (event_type == 'purchase'):
			# purchase
			id = info['id']
			timestamp = info['timestamp']
			amount = float(info['amount'])
			self.social_network.add_user(id)
			self.social_network.add_purchase(id, amount, timestamp)
			if is_init is True:
				return None

			history = self.social_network.get_tracked_purchase(
				id, self.degree, self.num_tracked)
			# calculate mean, std
			mean = np.mean(history)
			std = np.std(history)

			return (mean, std, amount)
		else:
			raise ValueError('Unexpected event_type: {}'.format(event_type))


		


