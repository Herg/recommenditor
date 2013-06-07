import sys
PATH_TO_PROJECT = "/Users/Herg/Documents/Projects/recommenditor/recommenditor"
sys.path.append(PATH_TO_PROJECT)

from datetime import datetime
import requests
import json
from lib.validation import validate_request


# only supports requests limits of < 100 or otherwise
# increments of 100
def make_get_request(redditor, **kwargs):
    limit = 100
    if "limit" in kwargs:
        limit = kwargs["limit"]
        if kwargs["limit"] > 100:
            kwargs["limit"] == 100
    # number of times to poll reddit for data, max items
    # we can grab at one time = 100
    repeat = limit / 100
    #  handle the case that they ask for < 100 items
    if repeat == 0:
        repeat = 1
    # url gets popped in each get request, need to save it
    # here to add back in on each call
    url = kwargs["url"]
    after = None
    if "after" in kwargs:
        after = kwargs["after"]
    # pass back list of data objects revieved from reddit
    data = []
    for rot in range(repeat):
        if after is not None:
            kwargs["after"] = after
        kwargs["url"] = url
        res = get_request_helper(redditor, **kwargs)
        if res["status"] == 1:
            data.append(res["data"])
            if "after" in res["data"]:
                after = res["data"]["after"]
            else:
                # we've hit the end of data to be retrieved before
                # the requested limit is up. gotta stop polling
                break
        else:
            # need to add some sort of functonality in the case where
            # one or more of the sub queries failed
            pass

    return {"status": 1, "data": data}


@validate_request
def get_request_helper(redditor, **kwargs):
    redditor.last_request = datetime.now()
    res = redditor.client.get(kwargs.pop("url"), params=kwargs)
    try:
        j = json.loads(res.text)
    except:
        return {
            "status": 0,
            "errmsg": "Server error, please try again"
        }

    return {"status": 1, "data": j["data"]}


@validate_request
def make_post_request(redditor, **kwargs):
    redditor.last_request = datetime.now()
    res = redditor.client.post(kwargs.pop("url"), data=kwargs)
    try:
        j = json.loads(res.text)
    except:
        return {
            "status": 0,
            "errmsg": "Server error, please try again"
        }

    return {"status": 1, "data": j["json"]["data"]}