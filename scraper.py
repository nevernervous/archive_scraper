from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import re
import json


def google_search(url):
    html = url.split()
    html = "+".join(html)
    req = urllib.request.Request(html, headers={'User-Agent': 'Mozilla/5.0'})

    soup = BeautifulSoup(urlopen(req).read(), "html.parser")

    # Regex
    reg = re.compile(".*&sa=")

    links = []
    # Parsing web urls
    for item in soup.find_all('h3', attrs={'class': 'r'}):
        line = (reg.match(item.a['href'][7:]).group())
        links.append(line[:-4])

    return links


def get_archive_metadata(url):
    url = url.replace('/details', '/metadata', 1)
    url += '/metadata'
    metadata = json.loads(urlopen(url).read().decode())
    catalog_number = metadata['result']['external-identifier'][1]
    catalog_number = catalog_number[catalog_number.rfind(':') + 1:]
    return {
        'title': metadata['result']['title'],
        'creator': metadata['result']['creator'][0],
        'publisher': metadata['result']['publisher'],
        'catalogNumber': catalog_number
    }
