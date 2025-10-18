# Fake Job Scraper

This project is a simple Python application that scrapes job postings from a specified website and saves the results to a CSV file named `fake_jobs.csv`. 

## Project Structure

```
fake-job-scraper
├── src
│   ├── scrape_jobs.py      # Main script to initiate the job scraping process
│   ├── scraper.py          # Contains the JobScraper class for scraping job postings
│   └── __init__.py         # Marks the directory as a Python package
├── tests
│   └── test_scraper.py     # Unit tests for the JobScraper class
├── requirements.txt         # Lists the project dependencies
├── .gitignore               # Specifies files to ignore in Git
└── README.md                # Documentation for the project
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd fake-job-scraper
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the job scraper, execute the following command:
```
python src/scrape_jobs.py
```

This will initiate the scraping process and create a file named `fake_jobs.csv` in the project directory containing the scraped job postings.

## Testing

To run the unit tests for the `JobScraper` class, use the following command:
```
python -m unittest discover -s tests
```

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements for the project.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.