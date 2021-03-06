
import time
from datetime import datetime


def validate_request(func):
    def decorator(redditor_obj, **kwargs):
        if "url" not in kwargs:
            return {
                "status": 0,
                "errmsg": "No URL given"
            }
        now = datetime.now()
        diff = now - redditor_obj.last_request
        # rate limiting, cannot make more than two requests
        # per second, sleep if it has been less than half
        # a second since our last request
        if diff.microseconds < 2000000:
            time.sleep(float((2000000 - diff.microseconds) / 1000000))
        return func(redditor_obj, **kwargs)
    return decorator
