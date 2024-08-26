import argparse
import logging
import os
from typing import Dict
import nltk
from bs4 import BeautifulSoup

from file_manager import FileManager
from web_scraper import EnhancedWebScraper
from summarizer import AdvancedSummarizer, create_meta_summary

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Download NLTK data
def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        logging.info("Downloading required NLTK data...")
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        logging.info("NLTK data downloaded successfully.")

def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get text
    text = soup.get_text()
    
    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    return text

def summarize_website(file_manager: FileManager, summarizer: AdvancedSummarizer) -> None:
    all_summaries = {}

    scraped_files = file_manager.get_scraped_files()
    logging.info(f"Found {len(scraped_files)} scraped files to summarize")

    if not scraped_files:
        logging.error("No scraped content found. Cannot generate summary.")
        return

    for file in scraped_files:
        file_path = os.path.join(file_manager.scraped_dir, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        logging.info(f"Summarizing {file}...")
        
        # Extract text from HTML
        text = extract_text_from_html(html_content)
        
        # Use the AdvancedSummarizer to summarize the extracted text
        summary = summarizer.summarize(text, ratio=0.3)  # Summarize to 30% of original length
        
        url = f"https://{file_manager.domain}/{file[:-4]}"  # Reconstruct URL
        all_summaries[url] = summary
        file_manager.save_summary(url, summary)

    # Create meta-summary
    meta_summary = create_meta_summary(all_summaries)
    file_manager.save_meta_summary(meta_summary)

    logging.info(f"Summary generated and saved. Total summarized pages: {len(all_summaries)}")

def main():
    parser = argparse.ArgumentParser(description="Enhanced Web Scraper and Summarizer")
    parser.add_argument("--url", type=str, required=True, help="URL of the website to scrape")
    parser.add_argument("--delay", type=float, default=1, help="Delay between requests in seconds (default: 1)")
    parser.add_argument("--use-selenium", action="store_true", help="Use Selenium for JavaScript rendering")
    parser.add_argument("--use-sitemap", action="store_true", help="Use sitemap for crawling")
    parser.add_argument("--max-pages", type=int, default=50, help="Maximum number of pages to scrape")
    args = parser.parse_args()

    # Download NLTK data
    download_nltk_data()

    logging.info(f"Starting enhanced web scraping for {args.url}...")
    
    file_manager = FileManager(args.url)
    scraper = EnhancedWebScraper(args.url, args.delay, args.use_selenium, args.max_pages)
    summarizer = AdvancedSummarizer()

    try:
        for url, content in scraper.crawl(use_sitemap=args.use_sitemap):
            logging.info(f"Scraped: {url}")
            file_manager.save_scraped_content(url, content)

        scraper.close()

        # Summarization process
        logging.info("Starting website summarization...")
        summarize_website(file_manager, summarizer)

        full_summary_path = os.path.join(file_manager.base_dir, f"{file_manager.domain}_FULL_SUMMARY.txt")
        if os.path.exists(full_summary_path):
            logging.info(f"Website summaries written to {file_manager.summary_dir}")
            logging.info(f"Full website summary written to {full_summary_path}")
            
            # Add the new message here
            print("\n" + "="*50)
            print("NEXT STEPS FOR A MORE HUMAN-READABLE SUMMARY:")
            print(f"1. Locate the file: {full_summary_path}")
            print("2. Drag and drop this file into Perplexity AI, Claude AI, or your preferred conversational AI tool.")
            print("3. Ask the AI to provide a concise, human-readable summary of the website based on the file's content.")
            print("This will give you a more coherent and easily digestible overview of the scraped website.")
            print("="*50 + "\n")
        else:
            logging.error(f"Failed to generate summary. Full summary file not found at {full_summary_path}")
            logging.info("Checking individual summary files...")
            summary_files = [f for f in os.listdir(file_manager.summary_dir) if f.endswith('_summary.txt')]
            if summary_files:
                logging.info(f"Found {len(summary_files)} individual summary files in {file_manager.summary_dir}")
            else:
                logging.error(f"No individual summary files found in {file_manager.summary_dir}")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()