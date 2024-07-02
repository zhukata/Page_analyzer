import validators
import requests


from urllib.parse import urlparse
from bs4 import BeautifulSoup


def parse_url(url):
    parse_dict = {}
    parse = requests.get(url).text
    soup = BeautifulSoup(parse, 'html.parser')
    parse_dict['description'] = find_description(soup)
    if soup.h1:
        parse_dict['h1'] = soup.h1.string
    if soup.title:
        parse_dict['title'] = soup.title.string
    return parse_dict


def find_description(soup):
    tag = soup.find('meta', content=True, attrs={"name": "description", })
    if tag:
        return tag['content']
    return ''


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
    except requests.exceptions.RequestException:
        return False
    return r.status_code
