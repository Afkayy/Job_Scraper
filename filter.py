import pandas as pd
import requests
import os
import csv
import time
import logging
import json
import re
import random

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_csv(filename='jobs.csv'):
    logger.info(f"Loading {filename}")
    try:
        df = pd.read_csv(filename)
        expected_columns = ['Title', 'Company', 'Location', 'Apply URL']
        if not all(col in df.columns for col in expected_columns):
            logger.error(f"Missing columns in {filename}. Expected: {expected_columns}")
            return None
        logger.info(f"Loaded {len(df)} jobs")
        return df
    except FileNotFoundError:
        logger.error(f"{filename} not found")
        return None
    except Exception as e:
        logger.error(f"Error reading CSV: {e}")
        return None

def parse_response(text):
    """Parse Gemini response, handling malformed JSON."""
    text = text.strip()
    # Clean text: remove ```json markers and ensure closing brace
    text = re.sub(r'^```json\n|\n```$', '', text)
    if not text.endswith('}'):
        text += '}'
    
    try:
        result = json.loads(text)
        return result.get('is_relevant', False)
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid JSON: {text[:100]}... Error: {e}")
        match = re.search(r'"is_relevant":\s*(true|false)', text, re.IGNORECASE)
        return match.group(1).lower() == 'true' if match else False

def is_job_relevant(title, api_key, max_retries=3):
    logger.info(f"Evaluating job: {title}")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    prompt = (
        f"Given the job title '{title}', determine if it is suitable for a fresh BS Computer Science graduate "
        "with expertise in Software Development, AI/ML, Deep Learning, and Web Development. "
        "Include 'junior' or 'entry-level' roles. Respond with JSON: {{'is_relevant': boolean}}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 50}
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if 'candidates' not in result or not result['candidates']:
                logger.error(f"No candidates for '{title}'")
                return False
            
            text = result['candidates'][0]['content']['parts'][0]['text']
            logger.debug(f"Raw response for '{title}': {text}")
            return parse_response(text)
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                delay = (2 ** attempt) + random.uniform(0, 0.1)
                logger.warning(f"Rate limit hit for '{title}'. Retrying in {delay:.2f}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
                continue
            logger.error(f"HTTP error for '{title}': {e}")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"API error for '{title}': {e}")
            return False
    
    logger.error(f"Max retries reached for '{title}'")
    return False

def pre_filter_title(title):
    """Pre-filter to reduce API calls."""
    relevant_keywords = [
        "software", "developer", "engineer", "ai", "machine learning", "ml",
        "deep learning", "web", "frontend", "backend", "full stack", "data scientist",
        "junior", "entry-level"
    ]
    return any(keyword in title.lower() for keyword in relevant_keywords)

def filter_jobs(df, api_key, max_jobs=50):
    logger.info("Starting job filtering")
    filtered_jobs = []
    processed = 0
    
    for idx, row in df.iterrows():
        if processed >= max_jobs:
            logger.info(f"Reached max_jobs limit ({max_jobs})")
            break
        
        title = row['Title']
        if not pre_filter_title(title):
            logger.debug(f"Skipped job (pre-filter): {title}")
            continue
        
        if is_job_relevant(title, api_key):
            filtered_jobs.append({
                'Title': row['Title'],
                'Company': row['Company'],
                'Location': row['Location'],
                'Apply URL': row['Apply URL']
            })
            logger.info(f"Added job: {title}")
        else:
            logger.debug(f"Skipped job: {title}")
        
        processed += 1
        time.sleep(5)  # Delay for rate limits
    
    logger.info(f"Filtered {len(filtered_jobs)} relevant jobs")
    return filtered_jobs

def save_to_csv(jobs, filename='filtered_jobs.csv'):
    logger.info(f"Attempting to save {len(jobs)} jobs to {filename}")
    if not jobs:
        logger.warning("No relevant jobs found to save")
        return

    headers = ['Title', 'Company', 'Location', 'Apply URL']
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            for job in jobs:
                writer.writerow(job)
        logger.info(f"Successfully saved to {filename}")
    except IOError as e:
        logger.error(f"Error saving CSV: {e}")

def main():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        logger.error("GEMINI_API_KEY not set")
        return

    df = load_csv()
    if df is None:
        return

    filtered_jobs = filter_jobs(df, api_key)
    save_to_csv(filtered_jobs)

if __name__ == "__main__":
    main()