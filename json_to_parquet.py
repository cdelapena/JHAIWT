import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

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

#Convert JSON to Pandas Dataframe and save as Parquet file
def json_to_parquet(json_data, parquet_file):
    if json_data is None:
        print("JSON data not retrieved.")
        return

    #Extract jobs data
    jobs = json_data.get('jobs', [])
    if not jobs:
        print("No jobs found in JSON data.")
        return
    
    #Define dataframe columns
    columns = ['url', 'title', 'company_name', 'category', 'location', 'description']
    
    # Create DataFrame
    data = []
    for job in jobs:
        description = strip_html_tags(job.get('description', ''))
        data.append([
            job.get('url', ''),
            job.get('title', ''),
            job.get('company_name', ''),
            job.get('category', ''),
            job.get('location', ''),
            description
        ])
    
    df = pd.DataFrame(data, columns=columns)
    
    #Save dataframe to Parquet
    try:
        df.to_parquet(parquet_file, index=False)
        print(f"Parquet file '{parquet_file}' created successfully.")
    except Exception as e:
        print(f"Error writing to Parquet file: {e}")

#Fetch JSON data from URL
json_data = get_json_data(url)

parquet_file = os.path.join('model_development', 'remotive_jobs.parquet')

#Convert JSON to DataFrame and save as Parquet
json_to_parquet(json_data, parquet_file)