from bs4 import BeautifulSoup
from urllib.request import urlopen
from myLogger import logger
from dateutil.parser import parse
import re
import json
import requests

discography_soups = {}


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

    # some case, title and publisher contains '-'.
    # but in the 78discography.com site, it may or not contain '-'.
    # to avoid this case, remove the space and '-'.

    catalog_number = metadata['result']['external-identifier'][1]
    catalog_number = catalog_number[catalog_number.rfind(':') + 1:]

    title = metadata['result']['title'].lower()
    title = title.replace(" ", "")
    title = title.replace("-", "")

    publisher = metadata['result']['publisher'].lower()
    publisher = publisher.replace(" ", "")
    publisher = publisher.replace("-", "")

    # creator info is not needed for searching date

    # if type(metadata['result']['creator']) is str:
    #     creator = metadata['result']['creator'].lower()
    # else:
    #     creator = metadata['result']['creator'][0].lower()

    data = {
        'title': title,
        # 'creator': creator,
        'publisher': publisher,
        'catalogNumber': catalog_number
    }

    # logger.info('publisher: {}\n catalog_number: {}\n title: {}\n creator: {}'.format(data['publisher'], data['catalogNumber'], data['title'], data['creator']))
    logger.info('publisher: {}\n catalog_number: {}\n title: {}'.format(data['publisher'], data['catalogNumber'], data['title']))
    return data


def scrape_78discography(archive_url, url):
    date = ''
    metadata = get_archive_metadata(archive_url)
    soup_key = url[url.rfind('/') + 1:]
    soup_key = soup_key[:soup_key.rfind('.')]

    soup = None

    if soup_key in discography_soups:
        soup = discography_soups[soup_key]
    else:
        soup = get_soup(url)
        discography_soups[soup_key] = soup

    # page title contains publisher name

    page_title = soup.title.string.lower()
    page_title = page_title.replace(" ", "")
    page_title = page_title.replace("-", "")

    if metadata['publisher'] not in page_title:
        page_title = soup.title.string.lower()
        page_title = page_title.split()[0]
        page_title = page_title.replace("-", "")

        if page_title not in metadata['publisher'] and metadata['publisher'] not in page_title:
            logger.warning('Publisher is not matched.')
            return ''

    ''' catalog_number example
        5686
        5686B
        5686 B
        20-4202
        No. 10287 --- https://archive.org/details/78_hot-tamale-mollie_al-bernard-weslyn--kortlander_gbia0002465a
    '''
    catalog_number = metadata['catalogNumber']
    catalog_number = catalog_number.replace(" ", "")
    catalog_number = catalog_number.replace("-", "")
    catalog_number = re.search('[a-zA-Z .]*(\d*)', catalog_number).group(1)

    for item in soup.find_all('td', text=re.compile('[a-zA-Z -]*({})'.format(catalog_number))):
        td_list = item.parent.select('td')

        # creator = td_list[1].string

        title = td_list[2].string.replace(" ", "")
        title = title.lower()
        title = title.replace("-", "")

        if metadata['title'] in title or title in metadata['title']:
            if len(td_list) == 8:
                date = date_parsing(td_list[6].string)
                break
            elif len(td_list) == 7:
                date = date_parsing(td_list[5].string)
                break

    if date is '':
        catalog_number = metadata['catalogNumber']
        for item in soup.find_all('td', text=catalog_number):
            td_list = item.parent.select('td')

            # creator = td_list[1].string

            title = td_list[2].string.replace(" ", "")
            title = title.lower()
            title = title.replace("-", "")

            if metadata['title'] in title or title in metadata['title']:
                if len(td_list) == 8:
                    date = date_parsing(td_list[6].string)
                    break
                elif len(td_list) == 7:
                    date = date_parsing(td_list[5].string)
                    break

    return date


def scrape_45worlds(archive_url, url):
    date = ''

    metadata = get_archive_metadata(archive_url)
    soup = get_soup(url)
    label_td = soup.find('td', text='Label:')
    if not label_td:
        return ''

    publisher = label_td.next_sibling.a.string.lower()
    publisher = publisher.replace(" ", "")
    publisher = publisher.replace("-", "")

    if not publisher.startswith(metadata['publisher']):
        logger.warning('Publisher is not matched.')
        return ''

    catalog_tr = label_td.parent.next_sibling.next_sibling
    catalog_number = catalog_tr.contents[1].string
    catalog_number = catalog_number.replace(" ", "")
    catalog_number = catalog_number.replace("-", "")
    if metadata['catalogNumber'] in catalog_number:
        date = date_parsing(catalog_tr.next_sibling.contents[1].string)
    else:
        logger.warning('catalogNumber is not matched.')

    return date


def date_parsing(date_string):
    if date_string == '' or date_string == '-' or date_string is None:
        return ''
    try:
        year = str(parse(date_string).year)
        year = year[2:]
    except ValueError:
        reg = re.compile('.*/.*/(.*)')
        m = reg.match(date_string)
        if not m:
            logger.warning('Date string is unknown string format.  {}'.format(date_string))
            return ''
        else:
            year = m.group(1)

    if not year:
        return ''

    return '19' + year

