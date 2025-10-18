import csv
from scraper import JobScraper

def main():
    job_scraper = JobScraper()
    job_postings = job_scraper.fetch_job_postings()
    job_scraper.write_to_csv(job_postings, 'fake_jobs.csv')

if __name__ == "__main__":
    main()