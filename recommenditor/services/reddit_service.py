
import sys
PATH_TO_PROJECT = "/Users/Herg/Documents/Projects/recommenditor/recommenditor"
sys.path.append(PATH_TO_PROJECT)

import requests
import json
from datetime import datetime
import time
from pprint import pprint
from lib.validation import validate_request
from lib.request import (make_post_request, make_get_request)


BASEURL = "http://www.reddit.com"


class redditor(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.last_request = datetime.now()
        self.client = requests.session()
        self.client.headers = {"user-agent": "/u/%s Magical Reddit Robot" % username}
        self.login(user=username, passwd=password, api_type="json")


    def login(self, **kwargs):
        kwargs["url"] = "%s%s" % (BASEURL, "/api/login")
        res = make_post_request(self, **kwargs)
        if res["status"] != 1:
            return None
        self.client.modhash = res["data"]["modhash"]
        self.client.user = self.username


    def get_subreddits(self, **kwargs):
        list_type = "popular"
        if "list_type" in kwargs:
            list_type = kwargs.pop("list_type")
        kwargs["url"] = "%s%s/%s/.json" % (BASEURL, "/subreddits", list_type)
        # pull down the subreddit data
        data = make_get_request(self, **kwargs)
        for resp_obj in data["data"]:
            pprint(resp_obj)



