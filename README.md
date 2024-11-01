---

# AI Web Scraper

![Streamlit](https://img.shields.io/badge/Streamlit-App-brightgreen) ![Python](https://img.shields.io/badge/Python-3.12-blue)

Welcome to **AI Web Scraper**, an advanced, AI-powered web scraping application that lets you extract and query information from any website! Simply enter a URL, and the app will scrape the site, retrieve its DOM content, and allow you to ask the AI specific questions about the information on that page.

## 🚀 Try the App

**[Live Demo on Streamlit!](https://aiwebber-c2w8dfibt3htpgwtpswmif.streamlit.app/)**

## 🌟 Features

- **URL-based Scraping**: Provide any URL, and the AI Web Scraper will grab the DOM content for you.
- **AI-Powered Query**: Enter a prompt to get detailed insights and responses directly from the webpage content.
- **Technologies**: Built using tools like **Selenium**, **BeautifulSoup**, **LangChain**, and more to ensure robust and flexible web scraping.
- **Streamlit UI**: Interactive and user-friendly interface powered by Streamlit.

## 🔍 How It Works

1. **Input the URL**: Paste the URL of the website you want to scrape into the app.
2. **Scrape the DOM**: The app retrieves the DOM content using Selenium and BeautifulSoup.
3. **Prompt the AI**: Enter your query, and the AI (powered by LangChain) will search the scraped content for relevant information and present an answer based on your prompt.

## ⚙️ Technologies Used

- **Selenium**: For navigating and interacting with websites.
- **BeautifulSoup**: For parsing HTML and extracting information from the DOM.
- **LangChain**: A framework that links language models for dynamic query responses.
- **Streamlit**: For a clean and interactive user interface.
- **Anthropic**: claude-3-5-sonnet-20240620 was used as the primary LLM.

## 🤖 Future Improvements

- **Enhanced AI Models**: Explore options to incorporate other language models for improved accuracy. (Put openai to the test)
- **Automated Data Pipelines**: Automatically refresh and update scraped content at set intervals. (create a weekly refresher to scrape sites)
- **Advanced Scraping Techniques**: Implement solutions to handle dynamic content and more complex sites. (etc like shopee)

---

Enjoy using the AI Web Scraper!
