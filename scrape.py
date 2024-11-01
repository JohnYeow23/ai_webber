import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import html.parser

from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By

load_dotenv()
    
SBR_WEBDRIVER = os.environ.get('BRIGHT_DATA')

def scrape_website(website):
    print("Launching chrome browser...")
    
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    print('Connecting to Scraping Browser...')
    
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        driver.get(website)
        print('Taking page screenshot to file page.png')
        driver.get_screenshot_as_file('./resources/page.png')
        print('Navigated! Scraping page content...')
        html = driver.page_source
        return html

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    
    cleaned_content = soup.get_text(separator='\n')
    # splitlines literally split each line of the text
    # `if line.strip()` will be false if it has empty spaces or whitespaces
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    
    return cleaned_content

# We need to split the text due to context windows that LLM have
# Maybe can explore the possibility of using langchain splitting functions to do the following!

def split_dom_content(dom_content, context_length= 200, max_length=6000):
    return [
        # dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length) -- Just pass in chunks
        dom_content[max(0, i - context_length) : i + max_length] for i in range(0, len(dom_content), max_length) # pass in chunks with context from the previous chunk
    ]