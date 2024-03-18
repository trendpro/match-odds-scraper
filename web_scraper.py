# web_scraper.py
import asyncio
import time
from playwright.async_api import async_playwright, TimeoutError


async def scrape_page(url):
    """Scrapes a webpage, scrolls to load content, intercepts JSON responses with 'fixture' in the URL,
    extracts HTML content of a specific div, and saves them to files.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        str: Representing the extracted HTML content.
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Navigate to the URL first
        await page.goto(url)

        try:
            page_title_selector = ".fixture-list-header > ms-tab-bar:nth-child(1) > ms-scroll-adapter:nth-child(1) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(1) > a:nth-child(1) > span:nth-child(1)"
            await page.wait_for_selector(page_title_selector, timeout=10000)  # Adjust timeout as needed
        except TimeoutError as e:
            print("Title not found within timeout.", e)

        # Scroll down to load more content
        while await is_scrolling_needed(page):
            print("Scrolling...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(3)

        # Extract HTML content of the div with class ".grid-wrapper"
        html_dump = await page.inner_html(".grid-wrapper")

        await browser.close()

    return html_dump

async def is_scrolling_needed(page):
    """Checks if further scrolling is needed based on the presence of the '.grid-footer > div:nth-child(1)' div.

    Args:
        page (playwright.Page): The Playwright page object.

    Returns:
        bool: True if further scrolling is needed, False otherwise.
    """

    try:
        # Wait for the div to appear with a short timeout (adjust as needed)
        await page.wait_for_selector(".grid-footer > div:nth-child(1)", timeout=2000)
        # If the div is found, consider it an indication of more content and return True
        return True
    except TimeoutError as e:
        print("Possibly reached end of infinite scroll", e)
        # If the div is not found within the timeout, assume no more content and return False
        return False
