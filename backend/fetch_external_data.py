from pathlib import Path
from typing import Dict
import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_request(src: str, url: str) -> Dict:
    """API getter

    Args:
        url (str): API target

    Returns:
        Dict: json body
    """
    print(f"Fetching data from {src}: {url}...")
    try:
        response = requests.get(url)
        print(f"\t->response status={response.status_code}")
        return response.json()
    except requests.exceptions.RequestException:
        raise


# Returning clean JSON from Remotive API
def return_clean_json_data(src: str , url: str) -> str:
    """TEMPORARY: Fetches and cleans the json body from remotive.com

    Args:
        src (str): source name i.e. remotive
        url (str): active API url
    """
    def strip_html_tags_and_decode(text: Dict) -> str:
        """Helper function to clean the response body.

        Args:
            text (Dict): response body as Python dictionary

        Returns:
            str: cleaned string of json body
        """
        soup = BeautifulSoup(text, "html.parser")
        return (
            soup.get_text(separator=" ", strip=True)
            .encode("ascii", "ignore")
            .decode("utf-8")
        )

    json_data = get_request(src, url)
    jobs = json_data.get("jobs", [])
    for job in jobs:
        job["description"] = strip_html_tags_and_decode(job.get("description", ""))
    return jobs


def fetch_external_data(api_sources: Path) -> pd.DataFrame:
    """Opens the api_sources data file and iteratively fetches
    results from the API.

    Args:
        api_sources (Path): api_sources.txt
            schema == "source_name,api_url\n"

    Returns:
        pd.DataFrame: the jobs_df; columns=[
            "url", "title", "company_name", "logo", "category", "tags", "job_type", "date_published", "required_location", "salary", "description", "source"
            ]
    """

    def get_remotive_jobs(url: str):
        """Remotive.com specifc data handler

        Args:
            url (str): up-to-date remotive.com API url
        """
        try:
            result = get_request("remotive", url)
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(
                f"ERROR: fetch_external_data.py: {e}"
            )

        print(
            f"Data source=remotive.com\n\t-> {result.get('job-count')} active records found."
        )
        print(f"\t-> data fields={result.get('jobs')[0].keys()}\n")
        remotive_df = pd.DataFrame(
            result.get("jobs"),
            columns=[
                "id",
                "url",
                "title",
                "company_name",
                "logo",
                "category",
                "tags",
                "job_type",
                "date_published",
                "required_location",
                "salary",
                "description",
            ],
        )
        remotive_df = remotive_df.drop(
            "id", axis=1
        )  # "id" is preserved in the url itself and is not useful to persist
        remotive_df["source"] = "remotive"
        remotive_df = remotive_df.explode("tags")
        remotive_df["description"] = remotive_df["description"].apply(
            lambda text: BeautifulSoup(text, "html.parser").get_text(
                separator=" ", strip=True
            )
        )
        remotive_df = remotive_df.astype(pd.StringDtype())
        return remotive_df

    with api_sources.open("r") as data_src_fh:
        for line in data_src_fh.readlines():
            src_data = line.split(",")
            src, url = src_data
            match src:
                case "remotive":
                    jobs_df = get_remotive_jobs(url)

    return jobs_df
