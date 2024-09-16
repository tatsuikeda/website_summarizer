# Website Scraper and Summarizer

This project provides an advanced tool for scraping websites and generating summaries of their content using state-of-the-art NLP techniques.

## Author

Tatsu Ikeda

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Features

- Web scraping with optional sitemap-only mode
- Advanced text summarization using BERT-based extractive techniques and TF-IDF
- Customizable summarization ratio
- Key phrase extraction
- Organized output with timestamps and metadata
- User-friendly command-line interface
- Support for both regular HTTP requests and Selenium for JavaScript-rendered content
- Cookie-based authentication for accessing content behind logins

## Dependencies

This project requires the following Python packages:

- requests
- beautifulsoup4
- selenium
- webdriver-manager
- nltk
- transformers
- torch
- scikit-learn
- numpy
- lxml
- html5lib
- tqdm
- python-magic
- python-magic-bin (for Windows users)

You can install all required packages using the provided `requirements.txt` file.

## Setting up a Virtual Environment

1. Ensure you have Python and pip installed on your system.

2. Install virtualenv if you haven't already:
   ```
   pip install virtualenv
   ```

3. Create a new virtual environment:
   ```
   python -m venv webscraper_env
   ```

4. Activate the virtual environment:
   - On Windows:
     ```
     webscraper_env\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source webscraper_env/bin/activate
     ```

5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

You can run the script using the following command:

```
python main.py --url https://example.com [OPTIONS]
```

Options:
- `--delay`: Set the delay between requests in seconds (default: 1)
- `--use-selenium`: Use Selenium for JavaScript rendering
- `--use-sitemap`: Use sitemap for crawling
- `--max-pages`: Set the maximum number of pages to scrape (default: 50)
- `--cookie-file`: Path to JSON file containing cookies for authentication

Example:
```
python main.py --url https://example.com --delay 2 --use-selenium --max-pages 100 --cookie-file path/to/cookies.json
```

### Using Cookies for Authentication

To scrape websites that require authentication, you can use the `--cookie-file` option. Create a JSON file with your cookies in the following format:

```json
[
  {
    "name": "cookie_name",
    "value": "cookie_value",
    "domain": ".example.com"
  },
  ...
]
```

You can obtain these cookies by logging into the website manually and then using browser developer tools to export the cookies.

## Output

The script creates a timestamped output directory for each run with the following structure:

```
output_[domain]_[timestamp]/
├── scraped_content/
│   ├── [page1].txt
│   ├── [page2].txt
│   └── ...
├── summaries/
│   ├── [page1]_summary.txt
│   ├── [page2]_summary.txt
│   └── ...
├── [domain]_FULL_SUMMARY.txt
└── metadata.json
```

## Acknowledgements

This project uses the following open-source libraries:
- [NLTK](https://www.nltk.org/) for natural language processing
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [Hugging Face Transformers](https://huggingface.co/transformers/) for BERT models
- [PyTorch](https://pytorch.org/) for deep learning computations
- [scikit-learn](https://scikit-learn.org/) for TF-IDF vectorization

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the issues page if you want to contribute.

## Disclaimer

This tool is for educational and research purposes only. Always respect website terms of service and robots.txt files when scraping. Ensure you have permission to scrape and summarize content from the target website. When using cookie-based authentication, make sure you have the right to access and scrape the content behind the login.

## Getting a Human-Readable Summary

After running the scraper and summarizer, you'll find a `[domain]_FULL_SUMMARY.txt` file in the output directory. For a more human-readable summary:

1. Locate the `[domain]_FULL_SUMMARY.txt` file in the output directory.
2. Drag and drop this file into Perplexity AI, Claude AI, or your conversational AI tool of choice.
3. Ask the AI to provide a concise, human-readable summary of the website based on the content of the file.

This step will help you get a more coherent and easily digestible overview of the scraped website content.