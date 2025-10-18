class JobScraper:
    def __init__(self, url):
        self.url = url
        self.job_postings = []

    def fetch_job_postings(self):
        import requests
        from bs4 import BeautifulSoup

        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Example scraping logic (this will need to be customized based on the actual website structure)
            for job in soup.find_all('div', class_='job-posting'):
                title = job.find('h2').text
                company = job.find('h3').text
                location = job.find('p', class_='location').text
                self.job_postings.append({
                    'title': title,
                    'company': company,
                    'location': location
                })
        else:
            print(f"Failed to retrieve jobs: {response.status_code}")

    def write_to_csv(self, filename='fake_jobs.csv'):
        import pandas as pd

        df = pd.DataFrame(self.job_postings)
        df.to_csv(filename, index=False)