import requests
import time
from functools import wraps

# Cache dictionary to store results with expiration time
cache = {}

def cache_result(func):
    @wraps(func)
    def wrapper(url):
        # Check if the result is cached and not expired
        if url in cache and time.time() - cache[url]['timestamp'] < 10:
            print(f"Using cached result for {url}")
            cache[url]['count'] += 1
            return cache[url]['content']
        else:
            print(f"Fetching fresh content for {url}")
            content = func(url)
            # Cache the result
            cache[url] = {'content': content, 'timestamp': time.time(), 'count': 1}
            return content
    return wrapper

@cache_result
def get_page(url: str) -> str:
    try:
        response = requests.get(url)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""

if __name__ == "__main__":
    # Test the get_page function
    for _ in range(5):
        print(get_page("http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com"))
        time.sleep(2)  # Wait for 2 seconds

