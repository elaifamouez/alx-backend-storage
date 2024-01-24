#!/usr/bin/env python3
"""
we will implement a get_page function
(prototype: def get_page(url: str) -> str:).
The core of the function is very simple.
It uses the requests module to obtain the HTML content of a particular URL
and returns it.

Start in a new file named web.py and do not reuse
the code written in exercise.py.

Inside get_page track how many times a particular URL was accessed
in the key "count:{url}" and cache the result with an expiration
time of 10 seconds.

Tip: Use http://slowwly.robertomurray.co.uk to simulate a slow response
and test your caching.
Bonus: implement this use case with decorators.
"""
import requests
from functools import wraps
import redis
from typing import Callable


def get_page(url: str) -> str:
    """
    This function uses the requests module to obtain the HTML
    content of a particular URL and returns it.
    """
    # create a redis instance
    redis_client = redis.Redis()

    # check if url is already cached
    cached_content = redis_client.get(url)
    if cached_content:
        return cached_content

    # get url html content
    page = requests.get(url)

    page_content = page.text

    # cache content and set an expiry time
    redis_client.setex(url, 10, page_content)

    # get number of time url is accessed
    url_count_key = f"count:{url}"
    redis_client.incr(url_count_key)

    return page_content
