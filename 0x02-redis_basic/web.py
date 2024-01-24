#!/usr/bin/env python3
"""
Module to create a web cache using Redis.
"""

import redis
import requests

# Create a Redis client
rc = redis.Redis()

# Initialize count
count = 0


def get_page(url: str) -> str:
    """
    Fetch a webpage and cache its content using Redis.

    Parameters:
    url (str): The URL of the webpage to fetch.

    Returns:
    str: The content of the webpage.
    """

    # Cache the count associated with the URL
    rc.set(f"cached:{url}", count)

    # Send a GET request to the URL
    resp = requests.get(url)

    # Increment the count associated with the URL
    rc.incr(f"count:{url}")

    # Set an expiration time on the cached count
    rc.setex(f"cached:{url}", 10, rc.get(f"cached:{url}"))

    # Return the text content of the webpage
    return resp.text


if __name__ == "__main__":
    # Fetch and cache a webpage
    get_page("http://slowwly.robertomurray.co.uk")
