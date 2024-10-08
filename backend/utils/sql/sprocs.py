from datetime import datetime, timezone
from pathlib import Path
import sqlite3
import time
from typing import List

from utils.sql.models import JobPosting, ModelData, JobCategory, JobTag
from utils.sql.sql import MultipleRecordsFound, NoRecordsFound


def get_connection(db_filename) -> sqlite3.Connection:
    # Get the absolute path to Job.db
    db_file = str(Path.cwd().resolve().joinpath("data").joinpath(f"{db_filename}"))
    return sqlite3.connect(db_file)


def timer(func: object):
    """Decorator that wraps sproc calls to the db used for monitoring performance

    Args:
        func (object): A function object
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"\t->Query returned in {execution_time:.4f} seconds")
        return result

    return wrapper


@timer
def get_all_job_postings(db_filename: str) -> list:
    """Gets unfiltered data for Browse table

    Args:
        db_filename (str): db for connection

    Returns:
        list: db records [id, title, description, category, company, salary, tags, job_type, url, publish_date, candidate_required_location]
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
                title,
                description,
                c.name,
                company_name,
                salary,
                GROUP_CONCAT(t.name, ', ') AS tags,
                job_type,
                url,
                publish_date,
                candidate_required_location
                FROM postings p
                    JOIN postingtags pt ON pt.posting_id = p.id
                    JOIN tags t ON t.id = pt.tag_id
                    JOIN categories c ON c.id = p.category_id
                WHERE p.inactive_date_utc = 'None'
                GROUP BY
                p.id,
                title,
                description,
                c.name,
                company_name,
                salary,
                job_type,
                url,
                publish_date,
                candidate_required_location
            """
        )
        postings = [
            JobPosting(
                id=row[0],
                title=row[1],
                description=row[2],
                category=row[3],
                company_name=row[4],
                salary=row[5],
                tags=row[6],
                job_type=row[7],
                url=row[8],
                publish_date=row[9],
                candidate_required_location=row[10],
            )
            for row in cursor.fetchall()
        ]

    print(f"getAllJobPostings returned {len(postings)} records.")
    return postings


@timer
def get_some_job_postings(db_filename: str, number: int) -> list:
    """Gets a certain number of results of unfiltered data for Browse table

    Args:
        db_filename (str): db for connection
        number (int): number of results to return

    Returns:
        list: a select number of db records [id, title, description, category, company, salary, tags, job_type, url, publish_date, candidate_required_location]
    """
    print("Getting connection to db...")
    conn = get_connection(db_filename)
    with conn:
        cursor = conn.cursor()

        print("Executing getSomeJobPostings sproc...")
        cursor.execute(
            f"""
            SELECT
                p.id,
                title,
                description,
                c.name,
                company_name,
                salary,
                GROUP_CONCAT(t.name, ', ') AS tags,
                job_type,
                url,
                publish_date,
                candidate_required_location
                FROM postings p
                    JOIN postingtags pt ON pt.posting_id = p.id
                    JOIN tags t ON t.id = pt.tag_id
                    JOIN categories c ON c.id = p.category_id
                WHERE p.inactive_date_utc = 'None'
                GROUP BY
                p.id,
                title,
                description,
                c.name,
                company_name,
                salary,
                job_type,
                url,
                publish_date,
                candidate_required_location
                LIMIT {str(number)}
            """
        )
        postings = [
            JobPosting(
                id=row[0],
                title=row[1],
                description=row[2],
                category=row[3],
                company_name=row[4],
                salary=row[5],
                tags=row[6],
                job_type=row[7],
                url=row[8],
                publish_date=row[9],
                candidate_required_location=row[10],
            )
            for row in cursor.fetchall()
        ]

    print(f"getSomeJobPostings returned {len(postings)} records.")
    return postings


@timer
def get_job_posting(job_id: int, db_filename: str) -> list:
    """Gets single record by id

    Args:
        job_id (int): [Job.db].[postings].id
        db_filename (str): db for connection

    Raises:
        MultipleRecordsFound: custom error class

    Returns:
        list: db record [id, title, description, category, company, salary, tags, job_type, url, publish_date, candidate_required_location]
    """
    query = f"""
            SELECT
                p.id,
                title,
                description,
                c.name,
                company_name,
                salary,
                GROUP_CONCAT(t.name, ', ') AS tags,
                job_type,
                url,
                publish_date,
                candidate_required_location
                FROM postings p
                    JOIN postingtags pt ON pt.posting_id = p.id
                    JOIN tags t ON t.id = pt.tag_id
                    JOIN categories c ON c.id = p.category_id
                WHERE p.inactive_date_utc = 'None'
                    AND p.id = {job_id}
                GROUP BY
                p.id,
                title,
                description,
                c.name,
                company_name,
                salary,
                job_type,
                url,
                publish_date,
                candidate_required_location
            """

    print("Getting connection to db...")
    conn = get_connection(db_filename)
    with conn:
        cursor = conn.cursor()
        cursor.execute(query)
        result = [
            JobPosting(
                id=row[0],
                title=row[1],
                description=row[2],
                category=row[3],
                company_name=row[4],
                salary=row[5],
                tags=row[6],
                job_type=row[7],
                url=row[8],
                publish_date=row[9],
                candidate_required_location=row[10],
            )
            for row in cursor.fetchall()
        ]

        if (n := len(result)) > 1:
            raise MultipleRecordsFound(expected=1, actual=n)
        elif n == 0:
            raise NoRecordsFound(expected=1, actual=0)
        return result[0]


@timer
def get_model_data_by_category(category_id: int, db_filename: str) -> list:
    """Gathers model-specific data by job category id

    Args:
        categories (int): Job.categories.id
        db_filename (str): db for connection

    Returns:
        list: db records [id, category, title, preprocessed_description, tags]
    """
    query = f"""
        SELECT
            p.id,
            c.name,
            title,
            preprocessed_description,
            GROUP_CONCAT(t.name, ', ') AS tags
            FROM categories c
                JOIN postings p ON P.category_id = c.id
                JOIN postingtags pt ON pt.posting_id = p.id
                JOIN tags t ON t.id = pt.tag_id
            WHERE p.inactive_date_utc = 'None'
                AND c.id = {category_id}
            GROUP BY
            p.id,
            c.name,
            title,
            preprocessed_description
        """

    print("Getting connection to db...")
    conn = get_connection(db_filename)
    with conn:
        cursor = conn.cursor()
        print(f"Executing getModelDataByCategory, ({category_id}) sproc...")
        cursor.execute(query)
        postings = [
            ModelData(
                id=row[0],
                category=row[1],
                title=row[2],
                preprocessed_description=row[3],
                tags=row[4],
            )
            for row in cursor.fetchall()
        ]

    print(f"getModelDataByCategory returned {len(postings)} records.")
    return postings


@timer
def get_recommended_job_postings(job_ids: List[int], db_filename: str) -> list:
    """Gets all recommended job postings

    Args:
        job_ids (List[int]): [[Job.db].[postings].id, ...]
        db_filename (str): db for connection

    Returns:
        list: db records [id, title, description, category, company, salary, tags, job_type, url, publish_date, candidate_required_location]
    """
    cast_to_string = [f"{i}" for i in job_ids]
    job_ids_str = ",".join(cast_to_string)

    query = f"""
            SELECT
                p.id,
                title,
                description,
                c.name,
                company_name,
                salary,
                GROUP_CONCAT(t.name, ', ') AS tags,
                job_type,
                url,
                publish_date,
                candidate_required_location
                FROM postings p
                    JOIN postingtags pt ON pt.posting_id = p.id
                    JOIN tags t ON t.id = pt.tag_id
                    JOIN categories c ON c.id = p.category_id
                WHERE p.inactive_date_utc = 'None'
                    AND p.id IN ({job_ids_str})
                GROUP BY
                p.id,
                title,
                description,
                c.name,
                company_name,
                salary,
                job_type,
                url,
                publish_date,
                candidate_required_location
            """

    print("Getting connection to db...")
    conn = get_connection(db_filename)
    with conn:
        cursor = conn.cursor()
        cursor.execute(query)
        result = [
            JobPosting(
                id=row[0],
                title=row[1],
                description=row[2],
                category=row[3],
                company_name=row[4],
                salary=row[5],
                tags=row[6],
                job_type=row[7],
                url=row[8],
                publish_date=row[9],
                candidate_required_location=row[10],
            )
            for row in cursor.fetchall()
        ]

        if len(result) == 0:
            raise NoRecordsFound(expected=1, actual=0)
        return result


@timer
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


@timer
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
