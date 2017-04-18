from bs4 import BeautifulSoup
from urllib.request import urlopen
from myLogger import logger
from dateutil.parser import parse
import re
import json
import requests


def get_soup(url):
    url = url.split()
    url = "+".join(url)
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36'})
    soup = BeautifulSoup(r.content, "html.parser")
    return soup


def google_search(url):
    links = []
    try:
        url = url.split()
        url = "+".join(url)
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 '})
        soup = BeautifulSoup(r.content, "html.parser")
        # Regex
        reg = re.compile(".*&sa=")

        # Parsing web urls
        for item in soup.find_all('h3', attrs={'class': 'r'}):
            line = (reg.match(item.a['href'][7:]).group())
            links.append(line[:-4])
    except Exception as e:
        logger.error('Google search error: {}'.format(e))

    return links


def get_archive_metadata(url):
    url = url.replace('/details', '/metadata', 1)
    url += '/metadata'
    metadata = json.loads(urlopen(url).read().decode())
    catalog_number = metadata['result']['external-identifier'][1]
    catalog_number = catalog_number[catalog_number.rfind(':') + 1:]
    return {
        'title': metadata['result']['title'].lower(),
        'creator': metadata['result']['creator'][0].lower(),
        'publisher': metadata['result']['publisher'].lower(),
        'catalogNumber': catalog_number.split()[0]
    }


def scrape_78discography(archive_url, url):
    date = ''
    metadata = get_archive_metadata(archive_url)
    soup = get_soup(url)
    publisher = soup.body.h1.center.string.lower()

    if not publisher.startswith(metadata['publisher'].lower()):
        logger.warning('Publisher is not matched.')
        return date

    for item in soup.find_all('td', text=metadata['catalogNumber']):
        td_list = item.parent.select('td')

        # creator = td_list[1].string

        title = td_list[2].string

        if title.lower() == metadata['title']:
            date = date_parsing(td_list[6].string)
            break

    return date


def scrape_45worlds(archive_url, url):
    date = ''

    metadata = get_archive_metadata(archive_url)
    soup = get_soup(url)
    # publisher = soup.body.h1.center.string.lower()
    return date


def scrpae_adp(archive_url, url):
    date = ''
    return date


def date_parsing(date_string):
    if date_string == '' or date_string == '-':
        return ''
    year = str(parse(date_string).year)

    if not year:
        return ''

    return '19' + year[2:]
