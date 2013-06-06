
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
        repeat = 1
        limit = 100
        if "limit" in kwargs:
            limit = kwargs["limit"]
        if "meta_limit" in kwargs:
            repeat = int(kwargs.pop("meta_limit")) / limit
        list_type = "popular"
        if "list_type" in kwargs:
            list_type = kwargs.pop("list_type")
        kwargs["url"] = "%s%s/%s/.json" % (BASEURL, "/subreddits", list_type)
        after = None
        if "after" in kwargs:
            after = kwargs["after"]

        subreddits = {}
        for rot in range(repeat):
            if after is not None:
                kwargs["after"] = after
            res = make_get_request(self, **kwargs)
            if res["status"] != 1:
                return res
            if "after" in res["data"]:
                after = res["data"]["after"]
            else:
                after = None
            for row in res["data"]["children"]:
                print row["data"]["title"]
            if after is None:
                return subreddits
        return {"status": 1, "after": after, "data": subreddits}



