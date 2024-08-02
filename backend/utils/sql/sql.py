from pathlib import Path
from datetime import datetime, timezone
import sqlite3
import pandas as pd
import numpy as np
from utils.data_cleaning.text_preprocessing import preprocess_text
from utils.sql.make_db import init_tables


class MultipleRecordsFound(Exception):
    """Exception raised when a query returns more records than expected."""

    def __init__(self, expected, actual, message="More records found than expected"):
        self.expected = expected
        self.actual = actual
        self.message = f"{message}: Expected {expected}, found {actual}"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class NoRecordsFound(Exception):
    """Exception raised when a query returns no results."""

    def __init__(self, expected, actual, message="No records found"):
        self.expected = expected
        self.actual = actual
        self.message = f"{message}: Expected {expected}, found {actual}"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


def insert_new_sources(df: pd.DataFrame, conn: sqlite3.Connection) -> None:
    """Adds new sources to the sources table with new PK

    Args:
        df (pd.DataFrame): jobs_df from fetch_external_data
        conn (sqlite3.Connection): inject dependency
    """
    # Select distinct sources from DataFrame to be inserted...
    source_df = df[["source"]]
    source_df = source_df.astype({"source": str})
    source_df = source_df.rename(columns={"source": "name"}).drop_duplicates(
        subset=["name"]
    )
    sources = set(source_df["name"].unique())

    # Check against records in db...
    current_sources = set()
    db_sources = pd.read_sql("SELECT name FROM sources GROUP BY name", conn)
    if not db_sources.empty:
        current_sources = set(db_sources["name"].unique())

    # Insert new...
    new_sources = list(sources - current_sources)
    if new_sources:
        print(f"\t-> Upserting {len(new_sources)} record(s) into [Job].[sources]...")
        new_sources_df = source_df[source_df["name"].isin(new_sources)]
        new_sources_df.to_sql("sources", conn, if_exists="append", index=False)
        conn.commit()
    else:
        print("\t->No new source records.")
    return


def insert_new_tags(df: pd.DataFrame, conn: sqlite3.Connection) -> None:
    """Adds new tags to the tags table with new PK

    Args:
        df (pd.DataFrame): jobs_df from fetch_external_data
        conn (sqlite3.Connection): inject dependency
    """
    # Select distinct tags from DataFrame to be inserted...
    tags_df = df[["tags"]]
    tags_df = tags_df.astype({"tags": str})
    tags_df = tags_df.rename(columns={"tags": "name"}).drop_duplicates(subset=["name"])
    tags = set(tags_df["name"].unique())

    # Check against records in db...
    current_tags = set()
    db_tags = pd.read_sql("SELECT name FROM tags GROUP BY name", conn)
    if not db_tags.empty:
        current_tags = set(db_tags["name"].unique())

    # Insert new...
    new_tags = list(tags - current_tags)
    if new_tags:
        print(f"\t-> Upserting {len(new_tags)} record(s) into [Job].[tags]...")
        new_tags_df = tags_df[tags_df["name"].isin(new_tags)]
        new_tags_df.to_sql("tags", conn, if_exists="append", index=False)
        conn.commit()
    else:
        print("\t->No new tag records.")
    return


def insert_new_categories(df: pd.DataFrame, conn: sqlite3.Connection) -> None:
    """Adds new categories to the categories table with new PK

    Args:
        df (pd.DataFrame): jobs_df from fetch_external_data
        conn (sqlite3.Connection): inject dependency
    """
    # Select distinct tags from DataFrame to be inserted...
    category_df = df[["category"]]
    category_df = category_df.astype({"category": str})
    category_df = category_df.rename(columns={"category": "name"}).drop_duplicates(
        subset=["name"]
    )
    categories = set(category_df["name"].unique())

    # Check against records in db...
    current_categories = set()
    db_categories = pd.read_sql("SELECT name FROM categories GROUP BY name", conn)
    if not db_categories.empty:
        current_categories = set(db_categories["name"].unique())

    # Insert new...
    new_categories = list(categories - current_categories)
    if new_categories:
        print(f"\t-> Upserting {len(new_categories)} record(s) into [Job].[tags]...")
        new_category_df = category_df[category_df["name"].isin(new_categories)]
        new_category_df.to_sql("categories", conn, if_exists="append", index=False)
        conn.commit()
    else:
        print("\t->No new category records.")
    return


def upsert_new_postings(df: pd.DataFrame, conn: sqlite3.Connection) -> None:
    """Upserts job postings into the postings table with new PK, and links
    to sources and tags table with appropriate FKs.

    Args:
        df (pd.DataFrame): jobs_df from fetch_external_data
        conn (sqlite3.Connection): inject dependency
    """
    url_df = df[["url"]].copy()

    # Inactive old records...
    urls_from_api = set(url_df["url"].unique())

    # Subtract records from the DB that are not in the API call
    active_urls = set()
    db_active_urls = pd.read_sql("SELECT url FROM postings WHERE inactive_date_utc = 'None' GROUP BY url", conn)
    if not db_active_urls.empty:
        active_urls = set(db_active_urls["url"])

    del db_active_urls

    inactivate = active_urls - urls_from_api

    # Constrain inactivation df to proper subset and set datetime
    if inactivate:
        quant = len(inactivate)
        print(f"\t-> Inactivating {quant} record(s) in [Job].[postings]...")
        # Batchify updates
        batch_size = 200
        url_batches = [list(inactivate)[i:i+batch_size] for i in range(0, quant, batch_size)]

        inactive_date = datetime.now(timezone.utc)

        # Update db records with SQL command
        inactivate_sql = """
UPDATE postings
SET inactive_date_utc = ?
WHERE url = ?
"""
        cursor = conn.cursor()
        for batch in url_batches:
            inactivate_data = [(inactive_date, url) for url in batch]
            cursor.executemany(inactivate_sql, inactivate_data)
            conn.commit()
        cursor.close()

    else:
        print("\t-> No previous postings require inactivation...")

    # Constrain full df to only new records from API call
    new_urls = urls_from_api - active_urls - inactivate

    new_df = df[df["url"].isin(new_urls)]
    posting_tag_df = new_df[["url", "tags"]].copy() # Save for a bit...

    new_df = new_df.drop("tags", axis=1).drop_duplicates()
    if len(new_df) > 0:
        print(f"\t-> {len(new_df)} valid new postings have been found. Preparing for ingestion...")

        # Add the tags FK to the df...
        source_df = pd.read_sql("SELECT id, name FROM sources;", conn)
        source_df["name"] = source_df["name"].astype(pd.StringDtype())

        new_df = new_df.rename(columns={"source": "name"})

        print("\t-> Getting [Job].[sources] FKs...")
        new_df = new_df.merge(source_df, on="name", how="inner")
        new_df = new_df.drop("name", axis=1)
        new_df = new_df.rename(columns={"id": "source_id"})

        del source_df

        # Add the category FK to the df...
        category_df = pd.read_sql("SELECT id, name FROM categories;", conn)
        category_df["name"] = category_df["name"].astype(pd.StringDtype())

        new_df = new_df.rename(columns={"category": "name"})

        print("\t-> Getting [Job].[categories] FKs...")
        new_df = new_df.merge(category_df, on="name", how="inner")
        new_df = new_df.drop("name", axis=1)
        new_df = new_df.rename(columns={"id": "category_id"})

        del category_df

        # Add timestamps...
        utc_now = datetime.now(timezone.utc)
        new_df["active_date_utc"] = utc_now.strftime("%Y-%m-%dT%H:%M:%SZ")
        new_df["active_date_utc"] = new_df["active_date_utc"].astype(pd.StringDtype())
        new_df["inactive_date_utc"] = None
        new_df["inactive_date_utc"] = new_df["inactive_date_utc"].astype(pd.StringDtype())

        # Final cleaning of the df
        new_df = new_df.drop("logo", axis=1)
        new_df = new_df.rename(columns={"date_published": "publish_date",})
        new_df.fillna(value="None", inplace=True)

        # Add a temporary ID for processing
        new_df["temp_id"] = new_df.index

        # Preprocess the descriptions before upserting
        print("\t->Preprocessing description text for use by recommendation engine...")
        try:
            descriptions_preprocessed = preprocess_text(new_df[["temp_id", "description"]])
        except Exception as e:
            print(f"Error during preprocessing: {e}")
            raise

        try:
            df_preprocessed = pd.DataFrame(descriptions_preprocessed)
        except Exception as e:
            print(f"Error creating DataFrame from preprocessed descriptions: {e}")
            raise

        try:
            new_df = new_df.merge(
                df_preprocessed[["temp_id", "preprocessed_description"]], on="temp_id"
            )
            new_df.drop("temp_id", axis=1, inplace=True)
        except Exception as e:
            print(f"Error merging preprocessed descriptions: {e}")
            raise
        print("\t->preprocessed_description field complete.")

        # Convert DataFrame to a list of tuples
        postings = new_df.to_records(index=False).tolist()

        # Prepare the SQL statement
        columns = ", ".join(new_df.columns)
        placeholders = ", ".join(["?" for _ in new_df.columns])
        conflict_update = ", ".join(
            [f"{col} = excluded.{col}" for col in new_df.columns if col != "url"]
        )

        sql = f"""
    INSERT INTO postings ({columns})
    VALUES ({placeholders})
    ON CONFLICT(id) DO UPDATE SET
        {conflict_update}
    """

        # Execute the upsert
        print(f"\t-> Upserting {len(new_df)} record(s) into [Job].[postings]...")
        cursor = conn.cursor()
        cursor.executemany(sql, postings)
        conn.commit()

        # M-2-M postings <-> tags insertion...
        insert_posting_tags(posting_tag_df, conn)
    else:
        print("\t->No new posting records.")
    return


def insert_posting_tags(df: pd.DataFrame, conn: sqlite3.Connection) -> None:
    """Inserts new records into intersection table for M-2-M postings <-> tags

    Args:
        df (pd.DataFrame): new postings ONLY
        conn (sqlite3.Connection): inject dependency
    """
    # Gather posting.id for new postings
    db_postings = pd.read_sql("SELECT id, url FROM postings WHERE inactive_date_utc = 'None' GROUP BY id, url", conn)
    posting_tag_df = df[["url", "tags"]].copy()
    posting_tag_df = posting_tag_df.merge(db_postings, on=["url"], how="inner")
    posting_tag_df = posting_tag_df.drop("url", axis=1)
    posting_tag_df = posting_tag_df.rename(columns={"id": "posting_id"})

    # Gather tag.id for new postings
    db_tags = pd.read_sql("SELECT id, name FROM tags GROUP BY id, name", conn)
    db_tags = db_tags.rename(columns={"name": "tags"})
    posting_tag_df = posting_tag_df.merge(db_tags, on=["tags"], how="inner")
    posting_tag_df = posting_tag_df.drop("tags", axis=1)
    posting_tag_df = posting_tag_df.rename(columns={"id": "tag_id"})


    print(f"\t-> Inserting {len(posting_tag_df)} record(s) into [Job].[postingtags]...")
    posting_tag_df.to_sql("postingtags", conn, if_exists="append", index=False)
    conn.commit()
    return


def db_ingestion(df: pd.DataFrame, db_filename: str = "Job.db") -> None:
    """Ingests records from API call into SQLite database

    Args:
        df (pd.DataFrame): data from API call
        db_filename (str, optional): SQLite db file name. Defaults to "Job.db".
    """
    # Get the absolute path to Job.db
    db_file = str(Path.cwd().resolve().joinpath("data").joinpath(f"{db_filename}"))

    # Create Connection
    print(f"Connecting to: {db_file}...")
    jobs_conn = sqlite3.connect(db_file)

    with jobs_conn:
        cursor = jobs_conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' and name='postings';"
        )

        active_listings = cursor.fetchall()

        if not active_listings:
            print(f"\t->{db_filename} does not yet exist.")
            print("\t-> Initializing the db...")
            init_tables(jobs_conn)
            print(f"\t->Initializing complete. {db_filename} is ready for ingestion.\n")

        print(f"Inserting [{db_filename.split('.')[0]}].[sources] table...")
        insert_new_sources(df, jobs_conn)

        print(f"Inserting [{db_filename.split('.')[0]}].[categories] table...")
        insert_new_categories(df, jobs_conn)

        print(f"Inserting [{db_filename.split('.')[0]}].[tags] table...")
        insert_new_tags(df, jobs_conn)

        print(f"Upserting [{db_filename.split('.')[0]}].[postings] table...")
        upsert_new_postings(df, jobs_conn)

        print("db ingestion complete.")
    return
