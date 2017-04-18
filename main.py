from myLogger import logger
import scraper

sites = ['http://www.78discography.com/', 'http://www.45worlds.com/78rpm/', 'http://adp.library.ucsb.edu/']


def get_certain_link(links):
    for link in links:
        for i in range(len(sites)):
            if link.startswith(sites[i]):
                return i, link
    return -1, None


def main():
    archive_details_urls = []
    google_search_urls = []
    with open('78dates.txt', mode='r', encoding='utf-8') as f:
        row_number = 1
        for row in f:
            data = row.split('\t')
            row_number += 1
            if len(data) != 3:
                logger.warning('Input data in {:d} row is not valid.'.format(row_number))
                continue

            if data[0]:
                continue

            archive_details_urls.append(data[1])
            google_search_urls.append(data[2])

    failed_file = open('failed.csv', 'w')

    with open('result.txt', 'w') as f:
        for i in range(len(archive_details_urls)):
            logger.info('Searching for -- {} --: {}'.format(i, archive_details_urls[i]))
            links = scraper.google_search(google_search_urls[i])
            if len(links) == 0:
                logger.warning('No search results.')
                continue

            site_index, link = get_certain_link(links)
            if site_index == -1:
                logger.warning('No matched site.')
                failed_file.write('{},{}'.format(archive_details_urls[i], google_search_urls[i]))
                continue

            logger.info('Matched site: {}'.format(link))

            date = ''

            if site_index == 0:
                continue
                date = scraper.scrape_78discography(archive_details_urls[i], link)
            elif site_index == 1:
                date = scraper.scrape_45worlds(archive_details_urls[i], link)
                break
            elif site_index == 2:
                date = scraper.scrpae_adp(archive_details_urls[i], link)
                break

            if date == '':
                logger.warning('Date not found.')
            else:
                logger.info('Date: {}'.format(date))

            f.write('{}\t{}\t{}'.format(archive_details_urls[i], date, link))





if __name__ == '__main__':
    main()


