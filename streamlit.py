'''
    1) Create the virtual environment, using pipenv install
    2) pip install streamlit langchain langchain_ollama selenium beautifulsoup4 lxml html5lib python-dotenv
'''
import os
import streamlit as st
from dotenv import load_dotenv

from bs4 import BeautifulSoup
import html.parser

from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

claude = ChatAnthropic(
    model="claude-3-5-sonnet-20240620",
    api_key=os.getenv("CLAUDE_API_KEY")
)

trace = os.getenv("LANGCHAIN_TRACING_V2")
langsmith = os.getenv("LANGCHAIN_API_KEY")

SBR_WEBDRIVER = os.environ.get('BRIGHT_DATA')

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return the following string ('Nothing found')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

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

'''
    We need to split the text due to context windows that LLM have
    Maybe can explore the possibility of using langchain splitting functions to do the following chunk splitting
'''

def split_dom_content(dom_content, context_length= 200, max_length=6000):
    return [
        # dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length) -- Just pass in chunks
        dom_content[max(0, i - context_length) : i + max_length] for i in range(0, len(dom_content), max_length) # pass in chunks with context from the previous chunk
    ]

def parse_with_claude(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | claude
    
    parsed_results = []
    
    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        print(f"Parsed batch {i} of {len(dom_chunks)}")
        parsed_results.append(response.content)
    return "\n".join(str(msg) for msg in parsed_results)

# Creating the streamlit UI
def main():
    st.title("AI Web Scraper")
    url = st.text_input("Enter a Website URL:")

    if st.button("Scrape Site"):
        st.write("Scraping the website")
        
        result = scrape_website(url)
        body_content = extract_body_content(result)
        cleaned_content = clean_body_content(body_content)
        
        st.session_state.dom_content = cleaned_content
        
        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)

    if "dom_content" in st.session_state:
        parse_description = st.text_area("Describe what you want to parse?")
        
        if st.button("Parse Content"):
            if parse_description:
                st.write("Parsing the content")
                
                dom_chunks = split_dom_content(st.session_state.dom_content)
                result = parse_with_claude(dom_chunks, parse_description)
                st.write(result)

if __name__ == "__main__":
    main()