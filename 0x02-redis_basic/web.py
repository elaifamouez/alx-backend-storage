#!/usr/bin/env python3
''' this module implements function track how many times a url is called'''
import requests
import redis
from functools import wraps
from typing import Callable


def counter_fun(func: Callable) -> Callable:
    '''decorator to track how many times a url is called
    and cache but the cache expires in 10sec'''
    redis_client = redis.Redis()

    @wraps(func)
    def inner(url):
        '''innner function for wdecorator'''
        key = 'count:' + url
        redis_client.incr(key)

        cached_html = redis_client.get(url)
        if cached_html:
            return cached_html.decode("utf-8")

        result = func(url)
        redis_client.set(url, result, ex=10)
        redis_client.expire(url, 10)
        return result
    return inner


@counter_fun
def get_page(url: str) -> str:
    '''this function get a page and return the html of tha page'''
    html = requests.get(url).text
    return html


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
