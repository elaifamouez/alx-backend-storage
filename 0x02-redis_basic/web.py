#!/usr/bin/env python3
""" Model for the get_page function """
import redis
from requests import get


def get_page(url: str) -> str:
    """obtain the HTML content of a particular URL and returns it."""
    r = redis.Redis()
    content = r.get(url)
    name = f"count:{url}"
    r.incr(name)
    if content:
        return content.decode('utf-8')
    content = get(url)
    r.setex(url, 10, content.text)
    r.set(f'count:{url}', 0)
    return content.text
