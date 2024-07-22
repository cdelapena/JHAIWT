from pathlib import Path
from datetime import datetime, timezone
import sqlite3

from utils.sql.models import JobPosting


def get_connection(db_filename) -> sqlite3.Connection:
    # Get the absolute path to Job.db
    db_file = str(Path.cwd().resolve().joinpath("data").joinpath(f"{db_filename}"))
    return sqlite3.connect(db_file)


def get_all_job_postings(db_filename) -> str:
    """_summary_

    Args:
        db_filename (_type_): _description_

    Returns:
        str: _description_
    """
    print("Getting connection to db...")
    conn = get_connection(db_filename)
    with conn:
        cursor = conn.cursor()

        print("Executing getAllJobPostings sproc...")
        cursor.execute(
            """
            SELECT
                p.id,
                category,
                company_name,
                job_title,
                description,
                preprocessed_description,
                salary,
                group_concat(t.name, ', ') AS tags,
                job_type,
                source_url,
                publish_date
                FROM postings p
                    JOIN tags t ON t.id = p.tag_id
                WHERE p.inactive_date_utc IS NOT NULL
                GROUP BY
                p.id,
                category,
                company_name,
                job_title,
                description,
                preprocessed_description,
                salary,
                job_type,
                source_url,
                publish_date
            LIMIT 3
            """
        )
        postings = [
            JobPosting(
                id=row[0],
                category=row[1],
                company_name=row[2],
                job_title=row[3],
                description = row[4],
                preprocessed_description=row[5],
                salary=row[6],
                tags=row[7],
                job_type=row[8],
                source_url=row[8],
                publish_date=row[10],
            )
            for row in cursor.fetchall()
        ]

    print(f"getAllJobPostings returned {len(postings)} records.")
    return postings


def get_job_postings_by_category(categories: str, db_filename: str) -> str:
    """_summary_

    Args:
        categories (str): _description_
        db_filename (str): _description_

    Returns:
        str: _description_
    """
    items = [item.strip() for item in categories.split(",")]
    category_req = ", ".join(f"'{item}'" for item in items)

    print("Getting connection to db...")
    conn = get_connection(db_filename)
    with conn:
        cursor = conn.cursor()

        print(f"Executing getJobPostingsByCategory, ({category_req}) sproc...")
        query = (
            f"""
            SELECT
                p.id,
                category,
                company_name,
                job_title,
                description,
                preprocessed_description,
                salary,
                group_concat(t.name, ', ') AS tags,
                job_type,
                source_url,
                publish_date
                FROM postings p
                    JOIN tags t ON t.id = p.tag_id
                WHERE p.inactive_date_utc IS NOT NULL
                AND category IN ({category_req})
                GROUP BY
                p.id,
                category,
                company_name,
                job_title,
                description,
                preprocessed_description,
                salary,
                job_type,
                source_url,
                publish_date
            """
        )
        print(query)
        cursor.execute(query)
        postings = [
            JobPosting(
                id=row[0],
                category=row[1],
                company_name=row[2],
                job_title=row[3],
                description = row[4],
                preprocessed_description=row[5],
                salary=row[6],
                tags=row[7],
                job_type=row[8],
                source_url=row[9],
                publish_date=row[10],
            )
            for row in cursor.fetchall()
        ]

    print(f"getJobPostingsByCategory returned {len(postings)} records.")
    return postings


print(get_all_job_postings("Job.db"))
# print(get_job_postings_by_category("QA", "Job.db"))