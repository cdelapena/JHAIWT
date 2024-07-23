from pathlib import Path
from datetime import datetime, timezone
import sqlite3

from utils.sql.models import JobPosting, ModelData, JobCategory, JobTag
from utils.sql.sql import MultipleRecordsFound


def get_connection(db_filename) -> sqlite3.Connection:
    # Get the absolute path to Job.db
    db_file = str(Path.cwd().resolve().joinpath("data").joinpath(f"{db_filename}"))
    return sqlite3.connect(db_file)


def get_all_job_postings(db_filename: str) -> list:
    """Gets unfiltered data for Browse table

    Args:
        db_filename (str): db for connection

    Returns:
        list: db records [id, category, company, job_title, salary, tags, job_type, publish_date]
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
                job_title,
                description,
                c.name,
                company_name,
                preprocessed_description,
                salary,
                GROUP_CONCAT(t.name, ', ') AS tags,
                job_type,
                source_url,
                publish_date
                FROM postings p
                    JOIN tags t ON t.id = p.tag_id
                    JOIN categories c ON c.id = p.category_id
                WHERE p.inactive_date_utc IS NOT NULL
                GROUP BY
                p.id,
                job_title,
                description,
                c.name,
                company_name,
                preprocessed_description,
                salary,
                job_type,
                source_url,
                publish_date
            """
        )
        postings = [
            JobPosting(
                id=row[0],
                job_title=row[1],
                description=row[2],
                category=row[3],
                company_name=row[4],
                preprocessed_description=row[5],
                salary=row[6],
                tags=row[7],
                job_type=row[8],
                source_url=row[9],
                publish_date=row[10],
            )
            for row in cursor.fetchall()
        ]

    print(f"getAllJobPostings returned {len(postings)} records.")
    return postings


def get_job_posting(job_id: int, db_filename: str) -> list:
    """_summary_

    Args:
        job_id (int): _description_
        db_filename (str): _description_

    Raises:
        MultipleRecordsFound: _description_

    Returns:
        list: _description_
    """
    query = f"""
            SELECT
                p.id,
                job_title,
                description,
                c.name,
                company_name,
                preprocessed_description,
                salary,
                GROUP_CONCAT(t.name, ', ') AS tags,
                job_type,
                source_url,
                publish_date
                FROM postings p
                    JOIN tags t ON t.id = p.tag_id
                    JOIN categories c ON c.id = p.category_id
                WHERE p.inactive_date_utc IS NOT NULL
                    AND p.id = {job_id}
                GROUP BY
                p.id,
                job_title,
                description,
                c.name,
                company_name,
                preprocessed_description,
                salary,
                job_type,
                source_url,
                publish_date
            """

    print("Getting connection to db...")
    conn = get_connection(db_filename)
    with conn:
        cursor = conn.cursor()
        cursor.execute(query)
        result = [
            JobPosting(
                id=row[0],
                job_title=row[1],
                description=row[2],
                category=row[3],
                company_name=row[4],
                preprocessed_description=row[5],
                salary=row[6],
                tags=row[7],
                job_type=row[8],
                source_url=row[9],
                publish_date=row[10],
            )
            for row in cursor.fetchall()
        ]

        if (n := len(result)) > 1:
            raise MultipleRecordsFound(expected=1, actual=n)
        elif n == 0:
            return None
        return result[0]


def get_model_data_by_category(categories: str, db_filename: str) -> list:
    """Gathers model-specific data by job category name

    Args:
        categories (str): comma-sep string of categories
        db_filename (str): db for connection

    Returns:
        list: db records [id, category, job_title, description, tags]
    """
    items = [item.strip() for item in categories.split(",")]
    category_req = ", ".join(f"'{item}'" for item in items)

    query = f"""
        SELECT
            p.id,
            c.name,
            job_title,
            description,
            GROUP_CONCAT(t.name, ', ') AS tags
            FROM postings p
                JOIN tags t ON t.id = p.tag_id
                JOIN categories c ON c.id = p.category_id
            WHERE p.inactive_date_utc IS NOT NULL
                AND c.name IN ({category_req})
            GROUP BY
            p.id,
            c.name,
            job_title,
            description
        """

    print("Getting connection to db...")
    conn = get_connection(db_filename)
    with conn:
        cursor = conn.cursor()
        print(f"Executing getModelDataByCategory, ({category_req}) sproc...")
        cursor.execute(query)
        postings = [
            ModelData(
                id=row[0],
                category=row[1],
                job_title=row[2],
                description=row[3],
                tags=row[4],
            )
            for row in cursor.fetchall()
        ]

    print(f"getModelDataByCategory returned {len(postings)} records.")
    return postings


def get_categories(db_filename: str) -> list:
    """Gets complete list of categories and ids for populating form drop-downs

    Args:
        db_filename (str): db for connection

    Returns:
        list: db records [category]
    """
    print("Getting connection to db...")
    conn = get_connection(db_filename)
    with conn:
        cursor = conn.cursor()

        print("Executing getCategories sproc...")
        cursor.execute("SELECT id, name FROM categories GROUP BY id, name")
        categories = [JobCategory(id=row[0], name=row[1]) for row in cursor.fetchall()]

    print(f"getCategories returned {len(categories)} records.")
    return categories


def get_tags(db_filename: str) -> list:
    """Gets complete list of tags and ids for populating form

    Args:
        db_filename (str): db for connection

    Returns:
        list: db records [tag]
    """
    print("Getting connection to db...")
    conn = get_connection(db_filename)
    with conn:
        cursor = conn.cursor()

        print("Executing getTags sproc...")
        cursor.execute("SELECT id, name FROM tags GROUP BY id, name")
        tags = [JobTag(id=row[0], name=row[1]) for row in cursor.fetchall()]

    print(f"getTags returned {len(tags)} records.")
    return tags
