
import time
from datetime import datetime


def validate_request(func):
    def decorator(redditor_obj, **kwargs):
        if "url" not in kwargs:
            return {
                "status": 0,
                "errmsg": "No URL given"
            }
        if "limit" in kwargs and kwargs["limit"] > 100:
            return {
                "status": 0,
                "errmsg": "Maximum allowed limit is 100"
            }
        now = datetime.now()
        diff = now - redditor_obj.last_request
        # rate limiting, cannot make more than two requests
        # per second, sleep if it has been less than half
        # a second since our last request
        if diff.microseconds < 500000:
            time.sleep(float((500000 - diff.microseconds) / 1000000))
        return func(redditor_obj, **kwargs)
    return decorator
