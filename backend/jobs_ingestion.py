from pathlib import Path
import sys
from fetch_external_data import fetch_external_data
from utils.sql.sql import db_ingestion


def main() -> None:
    """Fetches external data and stores"""
    api_sources = Path.cwd().resolve().joinpath("data").joinpath("api_sources.txt")
    try:
        jobs_df = fetch_external_data(api_sources)
    except:
        raise

    # Begin ingestion...
    try:
        print("Beginning Job.db ingestion.")
        db_ingestion(jobs_df)
    except Exception as e:
        err_msg = f"ERROR: utils/sql/sql.py: {e}."
        raise RuntimeError(err_msg)
    return


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        err_msg = f"Ingestion failed: {e}"
        sys.exit(1, err_msg)
