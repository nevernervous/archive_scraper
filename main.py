from myLogger import logger
from datetime import datetime
import scraper
import sys
import os
import traceback

# sites = ['http://www.78discography.com/', 'http://www.45worlds.com/78rpm/']
sites = ['http://www.78discography.com/']


def get_certain_link(links):
    for i in range(len(sites)):
        for link in links:
            if link.startswith(sites[i]):
                return i, link
    return -1, None


def main(input_file_name=None):
    result_folder = os.path.join('result', datetime.now().strftime('%H_%M_%d_%m_%Y'))
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    archive_details_urls = []
    google_search_urls = []
    with open(input_file_name, mode='r', encoding='utf-8') as f:
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

    date_not_found_file = open(os.path.join(result_folder, 'date_not_found_file.txt'), 'w', encoding='utf-8')
    no_google_search_result_file = open(os.path.join(result_folder, 'no_google_search_result.txt'), 'w', encoding='utf-8')
    no_matched_site_file = open(os.path.join(result_folder, 'no_matched_site.txt'), 'w', encoding='utf-8')
    error_file = open(os.path.join(result_folder, 'error.txt'), 'w', encoding='utf-8')
    have_to_scraped_again = open(os.path.join(result_folder, 'have_to_scraped_again.txt'), 'w', encoding='utf-8')

    with open(os.path.join(result_folder, 'result.txt'), 'w', encoding='utf-8') as f:
        for i in range(len(archive_details_urls)):
            try:
                logger.info('Searching for -- {} --\n archive url: {}\n google_search_url: {}'.format(i+1, archive_details_urls[i], google_search_urls[i]))
                links = scraper.google_search(google_search_urls[i])
                if len(links) == 0:
                    logger.warning('No search results.')
                    no_google_search_result_file.write('\t{}\t{}\n'.format(archive_details_urls[i], google_search_urls[i]))
                    no_google_search_result_file.flush()
                    have_to_scraped_again.write('\t{}\t{}\n'.format(archive_details_urls[i], google_search_urls[i]))
                    have_to_scraped_again.flush()
                    continue

                site_index, link = get_certain_link(links)
                if site_index == -1:
                    logger.warning('No matched site.')
                    no_matched_site_file.write('\t{}\t{}\n'.format(archive_details_urls[i], google_search_urls[i]))
                    no_matched_site_file.flush()
                    have_to_scraped_again.write('\t{}\t{}\n'.format(archive_details_urls[i], google_search_urls[i]))
                    have_to_scraped_again.flush()
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
                    date_not_found_file.write('\t{}\t{}\n'.format(archive_details_urls[i], google_search_urls[i]))
                    date_not_found_file.flush()
                    have_to_scraped_again.write('\t{}\t{}\n'.format(archive_details_urls[i], google_search_urls[i]))
                    have_to_scraped_again.flush()
                    continue
                else:
                    logger.info('Date: {}'.format(date))

                f.write('{}\t{}\t{}\n'.format(date, archive_details_urls[i], link))
                f.flush()
            except KeyboardInterrupt:
                exit()
            except:
                logger.error(traceback.format_exc())
                error_file.write('\t{}\t{}\n'.format(archive_details_urls[i], google_search_urls[i]))
                have_to_scraped_again.write('\t{}\t{}\n'.format(archive_details_urls[i], google_search_urls[i]))
                have_to_scraped_again.flush()


if __name__ == '__main__':
    # input_file_name = input('Enter the 78 dates text file:')
    logger.info('Start Scraping.')
    # main(input_file_name)
    main()



