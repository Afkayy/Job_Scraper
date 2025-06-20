Job Listings Scraper and Filter
Overview
This Python project fetches job listings from the Arbeitnow API, saves them to a CSV file, and filters the jobs to identify opportunities relevant to a fresh BS Computer Science graduate with expertise in Software Development, AI/ML, Deep Learning, and Web Development. The filtering process uses the Gemini API to evaluate job titles and includes pre-filtering to optimize API usage.
Features

API Integration: 
Fetches job listings from the Arbeitnow job board API.
Uses the Gemini API to evaluate job relevance based on job titles.


Pagination Handling: Retrieves multiple pages of job listings (default: 3 pages).
Error Handling: Robust handling of network errors, API request issues, and malformed JSON responses.
Pre-Filtering: Uses keyword-based pre-filtering to reduce unnecessary API calls.
CSV Export: 
Saves all fetched jobs to jobs.csv.
Saves filtered relevant jobs to filtered_jobs.csv.


Rate Limiting: Includes delays (1s for Arbeitnow API, 5s for Gemini API) to respect rate limits.
Logging: Comprehensive logging for debugging and monitoring.

Requirements

Python 3.x
Required libraries:pip install pandas requests


A valid Gemini API key set as an environment variable (GEMINI_API_KEY).

Setup

Clone the repository:git clone https://github.com/yourusername/job-listings-scraper.git


Install dependencies:pip install pandas requests


Set the Gemini API key:export GEMINI_API_KEY='your-api-key-here'

Replace 'your-api-key-here' with your actual Gemini API key.

Usage

Run the job scraper to fetch jobs:python job_scraper.py

This generates jobs.csv with all fetched job listings.
Run the job filter to identify relevant jobs:python job_filter.py

This reads jobs.csv, filters relevant jobs, and saves them to filtered_jobs.csv.

File Structure

job_scraper.py: Fetches job listings from Arbeitnow API and saves to jobs.csv.
job_filter.py: Filters jobs from jobs.csv using the Gemini API and saves relevant jobs to filtered_jobs.csv.
jobs.csv: Output file containing all scraped job listings.
filtered_jobs.csv: Output file containing filtered relevant job listings.

Output

jobs.csv: Contains all fetched jobs with columns:
Title: Job title
Company: Company name
Location: Job location
Apply URL: URL to apply for the job


filtered_jobs.csv: Contains filtered jobs (same columns) relevant to a BS Computer Science graduate with expertise in Software Development, AI/ML, Deep Learning, and Web Development.

Notes

The script uses a pre-filter to check for keywords like "software," "developer," "AI," "junior," etc., to optimize Gemini API calls.
The Gemini API is queried with a maximum of 50 jobs by default (configurable via max_jobs in job_filter.py).
Modify the max_pages parameter in job_scraper.py to fetch more or fewer pages from the Arbeitnow API.
Ensure a stable internet connection to avoid request timeouts.
The Gemini API key must be set as an environment variable (GEMINI_API_KEY) to run job_filter.py.
Logs are generated for debugging, including API errors, rate limit retries, and job filtering decisions.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss improvements or bugs.
