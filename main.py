from myLogger import logger
from datetime import datetime
import scraper
import os
import traceback

# sites = ['http://www.78discography.com/', 'http://www.45worlds.com/78rpm/', 'http://adp.library.ucsb.edu/']
sites = ['http://www.78discography.com/', 'http://www.45worlds.com/78rpm/']


def get_certain_link(links):
    for i in range(len(sites)):
        for link in links:
            if link.startswith(sites[i]):
                return i, link
    return -1, None


def main():
    result_folder = os.path.join('result', datetime.now().strftime('%H_%M_%d_%m_%Y'))
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    archive_details_urls = []
    google_search_urls = []
    # with open('78dates.txt', mode='r', encoding='utf-8') as f:
    # with open('78dates_new.txt', mode='r', encoding='utf-8') as f:
    with open('test.txt', mode='r', encoding='utf-8') as f:
        row_number = 1
        for row in f:
            data = row.rstrip('\n').split('\t')
            row_number += 1
            if len(data) != 3:
                logger.warning('Input data in {:d} row is not valid.'.format(row_number))
                continue

            if data[0]:
                continue

            archive_details_urls.append(data[1])
            google_search_urls.append(data[2])

    failed_file = open(os.path.join(result_folder, 'failed.txt'), 'w')

    with open(os.path.join(result_folder, 'result.txt'), 'w') as f:
        for i in range(len(archive_details_urls)):
            try:
                logger.info('Searching for -- {} --\n archive url: {}\n google_search_url: {}'.format(i+1, archive_details_urls[i], google_search_urls[i]))
                links = scraper.google_search(google_search_urls[i])
                if len(links) == 0:
                    logger.warning('No search results.')
                    failed_file.write('\t{}\t{}\n'.format(archive_details_urls[i], google_search_urls[i]))
                    failed_file.flush()
                    continue

                site_index, link = get_certain_link(links)
                if site_index == -1:
                    logger.warning('No matched site.')
                    failed_file.write('\t{}\t{}\n'.format(archive_details_urls[i], google_search_urls[i]))
                    failed_file.flush()
                    continue

                logger.info('Matched site: {}'.format(link))

                date = ''

                if site_index == 0:
                    date = scraper.scrape_78discography(archive_details_urls[i], link)
                elif site_index == 1:
                    date = scraper.scrape_45worlds(archive_details_urls[i], link)
                elif site_index == 2:
                    date = scraper.scrpae_adp(archive_details_urls[i], link)
                if date == '':
                    logger.warning('Date not found.')
                    failed_file.write('\t{}\t{}\n'.format(archive_details_urls[i], google_search_urls[i]))
                    failed_file.flush()
                    continue
                else:
                    logger.info('Date: {}'.format(date))

                f.write('{}\t{}\t{}\n'.format(archive_details_urls[i], date, link))
                f.flush()
            except KeyboardInterrupt:
                exit()
            except:
                logger.error(traceback.format_exc())


if __name__ == '__main__':
    logger.info('Start Scraping.')
    main()



