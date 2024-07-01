import validators
from urllib.parse import urlparse

def is_valid(data):
    if validators.url(data) and len(data) <= 255:
        return True

def normalaize_url(data):
    url = urlparse(data)
    return f"{url.scheme}://{url.netloc}"

    