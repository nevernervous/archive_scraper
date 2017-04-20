# README #

### Python Install
    Python version >= 3.4 
    
### Run scraper
    pip install -r requriements.txt
    python main.py
    
    
### Project Structure
* main.py  :
* myLogger.py --- manage log file
* scraper.py --- including scrapng functtions
* requirements.txt --- dependency file

### Description

While scraping, log file is stored in `log\[time]` folder.
Mathced dates is stored in `result\[time]\result.txt` folder.

There are 6 files in the `result` folder.

######error.txt
While scraping, unknown error occurs due to unknown data format.
If it happens, record url is stored in this file.

###### no_google_search_result.txt
This file is for record that have no google search results.

###### no_matched_site.txt
For record that has google search results but search results is not matched with certain sites such as `http://www.78discography.com/`

###### date_not_found_file.txt
For record that has matched site but date is not founded due to publisher or catalog number or title is not matched.

##### have_to_scraped_again.txt 
All of the above record is stored.
You can use this file for next input file.

###### result.txt
Scraped date is stored to this file.







 

    
    
    