#!/usr/bin/env python3
"""
Scrape fake job postings and save them to fake_jobs.csv

This script demonstrates using BeautifulSoup's class-based find/find_all
features (see https://blog.apify.com/beautifulsoup-find-by-class/) to extract
job postings from the Real Python "fake jobs" demo page and write them to a CSV.

Output CSV: fake_jobs.csv
Columns (header): Job Title, Company, Location, Date Posted

Usage:
    python3 scripts/scrape_fake_jobs.py

Requirements:
    pip install requests beautifulsoup4

The script uses class-based selectors to extract:
    - Job Title: <h2 class="title">
    - Company: <h3 class="company">
    - Location: <p class="location">
    - Date Posted: <time> element (text content)

Each job is wrapped in a <div class="card-content"> container.
The script includes fallbacks for slight HTML variations to ensure robustness.
"""

from __future__ import annotations
import csv
import sys
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://realpython.github.io/fake-jobs/"
OUTPUT_CSV = "fake_jobs.csv"
CSV_HEADERS = ["Job Title", "Company", "Location", "Date Posted"]


def fetch_page(url: str) -> str:
    """
    Fetch HTML content from the given URL.
    
    Args:
        url: The URL to fetch
        
    Returns:
        The HTML content as a string
        
    Raises:
        requests.HTTPError: If the request fails
    """
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


def _get_text(elem) -> str:
    """
    Safely extract text from a BeautifulSoup element.
    
    Args:
        elem: A BeautifulSoup element or None
        
    Returns:
        The stripped text content, or empty string if elem is None
    """
    return elem.get_text(strip=True) if elem else ""


def parse_jobs(html: str) -> List[Dict[str, str]]:
    """
    Parse job postings from HTML content.
    
    Uses class-based find/find_all per https://blog.apify.com/beautifulsoup-find-by-class/
    to extract job data with fallbacks for HTML variations.
    
    Args:
        html: The HTML content to parse
        
    Returns:
        A list of dictionaries, each containing job data with keys:
        "Job Title", "Company", "Location", "Date Posted"
    """
    soup = BeautifulSoup(html, "html.parser")

    # The Real Python fake-jobs demo wraps each job card inside 
    # <div class="card-content">. We use class_ parameter for find_all
    # as demonstrated in https://blog.apify.com/beautifulsoup-find-by-class/
    job_cards = soup.find_all("div", class_="card-content")
    
    jobs = []
    for card in job_cards:
        # Extract job title from <h2 class="title">
        # Fallback: try "title" class first, then any h2
        title_elem = card.find("h2", class_="title") or card.find("h2")
        title = _get_text(title_elem)
        
        # Extract company from <h3 class="company">
        # Fallback: try "company" class first, then any h3
        company_elem = card.find("h3", class_="company") or card.find("h3")
        company = _get_text(company_elem)
        
        # Extract location from <p class="location">
        # Fallback: try "location" class first, then first p tag
        location_elem = card.find("p", class_="location") or card.find("p")
        location = _get_text(location_elem)
        
        # Extract date posted from <time> element
        # Fallback: try time tag first, then look for datetime attribute or text
        time_elem = card.find("time")
        if time_elem:
            # Prefer datetime attribute if available, else use text content
            date_posted = time_elem.get("datetime", "").strip() or _get_text(time_elem)
        else:
            date_posted = ""
        
        # Only add job if we have at least a title
        if title:
            jobs.append({
                "Job Title": title,
                "Company": company,
                "Location": location,
                "Date Posted": date_posted
            })
    
    return jobs


def write_csv(jobs: List[Dict[str, str]], filename: str) -> None:
    """
    Write job data to a CSV file.
    
    Args:
        jobs: List of job dictionaries
        filename: Output CSV filename
    """
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(jobs)


def main() -> int:
    """
    Main function to scrape jobs and save to CSV.
    
    Returns:
        0 on success, 1 on error
    """
    try:
        print(f"Fetching job postings from {SOURCE_URL}...")
        html = fetch_page(SOURCE_URL)
        
        print("Parsing job data...")
        jobs = parse_jobs(html)
        
        if not jobs:
            print("Warning: No jobs found on the page.", file=sys.stderr)
            return 1
        
        print(f"Found {len(jobs)} job postings.")
        
        print(f"Writing to {OUTPUT_CSV}...")
        write_csv(jobs, OUTPUT_CSV)
        
        print(f"Success! Job data saved to {OUTPUT_CSV}")
        return 0
        
    except requests.RequestException as e:
        print(f"Error fetching page: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
