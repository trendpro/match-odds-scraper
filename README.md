# Tennis Match Scraper

A demonstration scraper program which will scrape all of the tennis match odds available on the following website:
https://sports.bwin.com/

## How to Run

1. Activate venv `python -m venv venv`
1. Install requirements `pip3 install -r requirements.txt`
1. Run them main module `python3 main.py`

> Don't have time to run the program? Here's a sample actual output from the program. [/output/sample_extracted_data.json](/output/sample_extracted_data.json)

## Solution Explanation

Uses playwright to browse the betting site and get a HTML dump. Why playwright, the site is JS heavy and has infinite scroll, playwright handles these problems well. Then use bs4 to parse the HTML dump into a JSON file.

## Things to improve

1. Add unit tests
