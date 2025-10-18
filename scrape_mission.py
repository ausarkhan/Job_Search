#!/usr/bin/env python3
"""
Usage:
  python scrape_mission.py
    - scrapes the default XULA URL and a default other URL (Tulane example).

  python scrape_mission.py --other "https://example.edu/about/mission"
    - scrapes XULA plus the provided other-university URL.

  python scrape_mission.py --single "https://www.xula.edu/about/mission-values.html"
    - scrapes only the single URL you provide.

Notes:
 - Be polite: respect robots.txt and the target site's terms of use.
 - This script uses a browser-like User-Agent header.
"""

import requests
from bs4 import BeautifulSoup
import re
import argparse
from urllib.parse import urlparse
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; mission-scraper/1.0; +https://github.com/yourname)"
}

DEFAULT_XULA = "https://www.xula.edu/about/mission-values.html"
# Example other university URL (change if needed)
DEFAULT_OTHER = "https://tulane.edu/about/mission-vision-values"

def get_soup(url, timeout=15):
    resp = requests.get(url, headers=HEADERS, timeout=timeout)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def find_sentence_with_substring(text, substring):
    # Find sentence containing substring (case-insensitive)
    sub = substring.lower()
    # naive sentence split
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for s in sentences:
        if sub in s.lower():
            return s.strip()
    return None

def cleanup_text(t):
    # normalize whitespace
    return re.sub(r'\s+', ' ', t).strip()

def extract_from_editorarea(soup):
    areas = soup.select("div.editorarea")
    if not areas:
        return None
    combined = " ".join([cleanup_text(a.get_text(" ", strip=True)) for a in areas])
    # look for "founded by Saint"
    found = find_sentence_with_substring(combined, "founded by Saint")
    if found:
        return found
    # fallback: return first 2 paragraphs worth of text from editorarea
    return combined[:2000]  # truncated fallback

def keyword_paragraph_search(soup, keywords=("mission", "purpose", "vision")):
    # look for headings that mention "mission" then get next paragraph(s)
    for htag in ("h1","h2","h3","h4","h5","h6"):
        for h in soup.find_all(htag):
            txt = h.get_text(" ", strip=True).lower()
            if any(k in txt for k in keywords):
                # get next sibling paragraphs
                paragraphs = []
                sib = h.find_next_sibling()
                # collect up to 3 sibling paragraphs/text blocks
                count = 0
                while sib and count < 6:
                    if sib.name in ("p","div"):
                        paragraphs.append(cleanup_text(sib.get_text(" ", strip=True)))
                    sib = sib.find_next_sibling()
                    count += 1
                if paragraphs:
                    return " ".join(paragraphs)
    # fallback: search <p> tags for keywords
    for p in soup.find_all("p"):
        text = p.get_text(" ", strip=True)
        if any(k in text.lower() for k in keywords):
            return cleanup_text(text)
    return None

def generic_main_content_search(soup):
    # look for article/main sections and return the largest text block
    candidates = []
    for sel in ("main", "article", "section", "div.content", "div#content"):
        el = soup.select_one(sel)
        if el:
            candidates.append(cleanup_text(el.get_text(" ", strip=True)))
    if candidates:
        # pick the largest text block
        return max(candidates, key=len)
    # last resort: return first 2000 chars of the page text
    return cleanup_text(soup.get_text(" ", strip=True))[:2000]

def scrape_mission(url):
    try:
        soup = get_soup(url)
    except Exception as e:
        return {"url": url, "error": f"Request failed: {e}"}

    # 1) Try editorarea (hint from TODO)
    result = extract_from_editorarea(soup)
    if result:
        return {"url": url, "mission": result}

    # 2) Keyword-based paragraph search (mission/purpose/vision)
    result = keyword_paragraph_search(soup)
    if result:
        return {"url": url, "mission": result}

    # 3) Generic main/article search
    result = generic_main_content_search(soup)
    if result:
        return {"url": url, "mission": result}

    return {"url": url, "error": "No mission-like content found"}

def main():
    parser = argparse.ArgumentParser(description="Scrape mission statements")
    parser.add_argument("--other", "-o", help="Other university URL to scrape", default=DEFAULT_OTHER)
    parser.add_argument("--single", "-s", help="Scrape only this single URL (skips defaults)")
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds to wait between requests")
    args = parser.parse_args()

    urls = []
    if args.single:
        urls = [args.single]
    else:
        urls = [DEFAULT_XULA, args.other]

    results = []
    for u in urls:
        print(f"Scraping: {u}")
        res = scrape_mission(u)
        results.append(res)
        time.sleep(max(0.0, args.delay))

    # Pretty print results
    for r in results:
        print("-" * 72)
        print(f"URL: {r.get('url')}")
        if r.get("error"):
            print("Error:", r["error"])
        else:
            print("Mission snippet:")
            print(r["mission"])
    print("-" * 72)

if __name__ == "__main__":
    main()