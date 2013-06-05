
import sys
PATH_TO_PROJECT = "/Users/Herg/Documents/Projects/recommenditor/recommenditor"
sys.path.append(PATH_TO_PROJECT)

import requests
import json
from datetime import datetime
import time

from lib.validation import validate_request

BASEURL = "http://www.reddit.com/api"


class redditor(object):

	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.useragent = "/u/%s Magical Reddit Robot" % username
		self.last_request = datetime.now()
		self.client = self.login()


	@validate_request
	def login(self):
		client = requests.session()
		client.headers = {'user-agent': self.useragent}
		up_dict = {
			'user': self.username,
			'passwd': self.password,
			'api_type': 'json'
			}
		self.last_request = datetime.now()
		res = client.post("%s%s" % (BASEURL, "/login"), data=up_dict)
		try:
			j = json.loads(res.text)
		except:
			print str(sys.exc_info())
			return None
		client.modhash = j['json']['data']['modhash']
		client.user = self.username
		print client.modhash

		return client




