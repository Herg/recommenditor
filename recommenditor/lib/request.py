import sys
PATH_TO_PROJECT = "/Users/Herg/Documents/Projects/recommenditor/recommenditor"
sys.path.append(PATH_TO_PROJECT)

from datetime import datetime
import requests
import json
from lib.validation import validate_request



@validate_request
def make_get_request(redditor, **kwargs):
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