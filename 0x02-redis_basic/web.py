#!/usr/bin/env python3
'''In this tasks, we will implement a get_page
function (prototype: def get_page(url: str) -> str:). The core of the
function is very simple. It uses the requests module to obtain the HTML
content of a particular URL and returns it.

Start in a new file named web.py and do not reuse the code
written in exercise.py.

Inside get_page track how many times a particular URL was accessed
in the key "count:{url}" and cache the result with an expiration time
of 10 seconds.

Tip: Use http://slowwly.robertomurray.co.uk to simulate a slow response
and test your caching.
Bonus: implement this use case with decorators.
'''
import redis
from typing import Callable
from requests import get
from functools import wraps


def track_page_count(method: Callable) -> Callable:
    '''Tracks the number of times a URL is accessed'''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wrapper function'''
        cache = redis.Redis()
        url = args[0]
        key = "count:{}".format(url)
        cache.incr(key)
        page = cache.get(url)
        if page is not None:
            return page.decode('utf-8')
        page = method(self, *args, **kwargs)
        cache.setex(url, 10, page)
        return page
    return wrapper


def get_page(url: str) -> str:
    '''Gets the HTML content of a particular URL'''
    return get(url).text
