
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
        print "making request uno"
        data = make_get_request(self, **kwargs)
        clean_data = []
        for sub_cluster in data["data"]:
            for sub in sub_cluster["children"]:
                subreddit = sub["data"]
                date_created = str(datetime.utcfromtimestamp(subreddit["created_utc"]))
                subreddit_id = subreddit["name"]
                url = subreddit["url"]
                display_name = subreddit["display_name"]
                title = subreddit["title"]
                nsfw_str = subreddit["over18"]
                nsfw = 1
                if nsfw_str == False:
                    nsfw = 0
                public_description = subreddit["public_description"]
                subscribers = int(subreddit["subscribers"])
                clean_data.append([date_created,subreddit_id,url,display_name,title,nsfw,public_description,subscribers])
        return clean_data


    def get_subreddit_submission_authors(self, **kwargs):
        kwargs["url"] = "%s%s/top.json" % (BASEURL, kwargs.pop("subreddit_url"))
        data = make_get_request(self, **kwargs)
        authors = []
        for post_cluster in data["data"]:
            for post in post_cluster["children"]:
                authors.append([post["data"]["author"]])
        return authors


    def get_user_submissions(self, **kwargs):
        kwargs["url"] = "%s/user/%s/submitted.json" % (BASEURL, kwargs.pop("username"))
        data = make_get_request(self, **kwargs)
        submissions = []
        for posts in data["data"]:
            for submission_data in posts["children"]:
                submission = submission_data["data"]
                date_created = str(datetime.utcfromtimestamp(submission["created_utc"]))
                username = submission["author"]
                submission_id = submission["name"]
                subreddit_id = submission["subreddit_id"]
                submissions.append([date_created, username, submission_id, subreddit_id])
        return submissions


    def get_user_comments(self, **kwargs):
        kwargs["url"] = "%s/user/%s/comments.json" % (BASEURL, kwargs.pop("username"))
        data = make_get_request(self, **kwargs)
        comments_arr = []
        for comments in data["data"]:
            for comment_data in comments["children"]:
                comment = comment_data["data"]
                date_created = str(datetime.utcfromtimestamp(comment["created_utc"]))
                username = comment["author"]
                comment_id = comment["name"]
                subreddit_id = comment["subreddit_id"]
                comments_arr.append([date_created, username, comment_id, subreddit_id])
        return comments_arr

