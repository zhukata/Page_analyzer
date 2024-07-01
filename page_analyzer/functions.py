import validators
import requests


from urllib.parse import urlparse

def is_valid(data):
    if validators.url(data) and len(data) <= 255:
        return True


def normalaize_url(data):
    url = urlparse(data)
    return f"{url.scheme}://{url.netloc}"


def check_url(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.RequestException as ex:
        return False
    return r.status_code
