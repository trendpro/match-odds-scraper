# main.py
import asyncio

from html_parser import parse_html_dump, save_data_as_json
from web_scraper import scrape_page

if __name__ == "__main__":
    url = "https://sports.bwin.com/en/sports/tennis-5/betting"  # Replace with the URL of the page you want to scrape
    json_file_path = "output/extracted_data.json"

    # Scrape the page and get results
    html_dump = asyncio.run(scrape_page(url))

    extracted_data = parse_html_dump(html_dump)
    save_data_as_json(extracted_data, json_file_path)

    print("Data saved to", json_file_path)
