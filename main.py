import csv
from myLogger import logger
import scraper

sites = ['http://www.78discography.com/', 'http://www.45worlds.com/78rpm/', 'http://adp.library.ucsb.edu/']


def get_certain_link(links):
    for link in links:
        for site in sites:
            if link.startswith(site):
                return

if __name__ == '__main__':
    dates = []
    archive_details_urls = []
    google_search_urls = []

    with open('78dates.txt', 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        lineNumber = 1
        for row in f:
            data = row.split('\t')
            if len(data) != 3:
                logger.warning('Input data in {:d} lines is not valid.'.format(lineNumber))
                continue

            dates.append(data[0])
            archive_details_urls.append(data[1])
            google_search_urls.append(data[2])
            lineNumber += 1

    with open('result.txt', 'w') as f:
        for i in range(len(dates)):
            if not dates[i]:
                links = scraper.google_search(google_search_urls[i])
                print(google_search_urls[i])
                break



