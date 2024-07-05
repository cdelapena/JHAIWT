import requests
import csv
from bs4 import BeautifulSoup

# URL for fetching the JSON data
url = "https://remotive.com/api/remote-jobs"

#Fetch JSON data from URL
def get_json_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        print("Data fetched successfully from URL.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

#Strip HTML tags
def strip_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text(separator=" ", strip=True)

#Convert JSON to CSV
def json_to_csv(json_data, csv_file):
    if json_data is None:
        print("JSON data not retrieved.")
        return

    #Extract jobs data
    jobs = json_data.get('jobs', [])
    if not jobs:
        print("No jobs found in JSON data.")
        return
    
    #Define CSV columns
    columns = ['url', 'title', 'company_name', 'category', 'candidate_required_location', 'description']
    
    #Write to CSV
    try:
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(columns)
            for job in jobs:
                description = strip_html_tags(job.get('description', ''))
                writer.writerow([
                    job.get('url', ''),
                    job.get('title', ''),
                    job.get('company_name', ''),
                    job.get('category', ''),
                    job.get('candidate_required_location', ''),
                    description
                ])
        print(f"CSV file '{csv_file}' created successfully.")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")

# Fetch JSON data from URL
json_data = get_json_data(url)

# Convert JSON to CSV
json_to_csv(json_data, 'remotive_jobs.csv')