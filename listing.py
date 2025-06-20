import requests
import csv
import time

def get_jobs(max_pages=3):
    base_url = "https://www.arbeitnow.com/api/job-board-api"
    all_jobs = []
    page = 1

    while page <= max_pages:
        try:
            # Construct URL with pagination
            url = f"{base_url}?page={page}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Assuming jobs are in a 'data' key
            jobs = data.get('data', [])
            if not jobs:
                break

            # Collect all jobs without filtering
            for job in jobs:
                all_jobs.append({
                    'title': job.get('title', 'N/A'),
                    'company': job.get('company_name', 'N/A'),
                    'location': job.get('location', 'N/A'),
                    'apply_url': job.get('url', 'N/A')
                })

            page += 1
            time.sleep(1)  # Respect rate limits

        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break

    return all_jobs

def save_to_csv(jobs, filename='jobs.csv'):
    if not jobs:
        print("No jobs found to save.")
        return

    headers = ['Title', 'Company', 'Location', 'Apply URL']

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            for job in jobs:
                writer.writerow({
                    'Title': job['title'],
                    'Company': job['company'],
                    'Location': job['location'],
                    'Apply URL': job['apply_url']
                })
        print(f"Jobs saved to {filename}")
    except IOError as e:
        print(f"Error saving CSV: {e}")

def main():
    # Fetch all jobs
    jobs = get_jobs()
    
    # Save to CSV
    if jobs:
        save_to_csv(jobs)
    else:
        print("No jobs found.")

if __name__ == "__main__":
    main()