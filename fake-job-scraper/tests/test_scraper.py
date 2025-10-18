import unittest
from src.scraper import JobScraper

class TestJobScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = JobScraper()

    def test_fetch_job_postings(self):
        # Assuming the method fetch_job_postings returns a list of job postings
        postings = self.scraper.fetch_job_postings()
        self.assertIsInstance(postings, list)
        self.assertGreater(len(postings), 0)

    def test_write_to_csv(self):
        # Test writing to CSV
        test_data = [{'title': 'Test Job', 'company': 'Test Company', 'location': 'Test Location'}]
        self.scraper.write_to_csv(test_data, 'test_jobs.csv')
        
        # Check if the file was created and contains the expected data
        with open('test_jobs.csv', 'r') as file:
            lines = file.readlines()
            self.assertGreater(len(lines), 0)
            self.assertIn('Test Job', lines[1])
            self.assertIn('Test Company', lines[1])
            self.assertIn('Test Location', lines[1])

if __name__ == '__main__':
    unittest.main()