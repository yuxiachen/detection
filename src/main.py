from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import sys
import numpy as np

from detector import Detector


def main():
	if len(sys.argv) != 4:
		print('Usage: <script_name> <file path to batch log> <file path stream log>',
			  ' <file path to output file>')
		return

	batch_log_file = sys.argv[1]
	stream_log_file = sys.argv[2]
	output_file = sys.argv[3]
	
	with open(batch_log_file, 'r') as f:
		batch_lines = f.readlines()

	assert len(batch_lines) >= 1, (
		'Unexpected number of batch lines: {}'.format(len(batch_lines)))

	d_t_json = json.loads(batch_lines[0])
	D = int(d_t_json['D'])
	T = int(d_t_json['T'])

	detector = Detector(batch_lines[1:], D, T)

	output_f = open(output_file, 'w')
	# output float format

	with open(stream_log_file, 'r') as f:
		ln = f.readline()
		while ln:
			info = json.loads(ln)
			ret = detector.process_event(info)
			if ret is None:
				continue
			# must be purchase event
			assert info['event_type'] == 'purchase', (
				'Critical error: unexpected event type: {}'.format(info['event_type']))
			mean, std, amount = ret
			# check if it's abnormal
			# import pdb; pdb.set_trace()
			if (np.abs(mean - amount) > 3 * std):
				out_ln = '{}, "mean": "{:.2f}", "sd": "{:.2f}"}}'.format(
					ln[:-1], mean, std)
				output_f.write(out_ln)

			# read next line	
			ln = f.readline()

 	output_f.close()


if __name__ == '__main__':
	main()


