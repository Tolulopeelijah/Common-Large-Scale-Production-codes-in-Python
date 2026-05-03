"""
A decorator that wraps any function and automatically retries it up to N times if it raises an exception, with an exponential backoff between attempts — meaning the wait time doubles each retry: 1s, 2s, 4s, 8s... If all retries are exhausted it raises the last exception.
"""

import time
import random
from functools import wraps

def retry(times, base_delay=1, max_delay=60, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)                          # preserves func.__name__ and __doc__
        def wrapper(*args, **kwargs):
            error = None
            for n in range(times):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:       # only retry specified exception types
                    error = e
                    if n < times - 1:
                        delay = min(base_delay * 2 ** n, max_delay)
                        jitter = random.uniform(0, delay * 0.1)  # ±10% randomness
                        time.sleep(delay + jitter)
            raise error
        return wrapper
    return decorator


# # usage — only retry on connection errors, not on bad input
# @retry(times=4, base_delay=1, exceptions=(ConnectionError, TimeoutError))
# def call_llm(prompt):
#     return requests.post("https://api.openai.com/...", ...)