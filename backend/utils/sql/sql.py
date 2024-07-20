from pathlib import Path
from datetime import datetime, timezone
import sqlite3
import pandas as pd

from utils.sql.make_db import init_tables


def insert_new_sources(df: pd.DataFrame, conn: sqlite3.Connection) -> None:
    """Adds new sources to the sources table with new PK

    Args:
        df (pd.DataFrame): jobs_df from fetch_external_data
        conn (sqlite3.Connection): inject dependency
    """
    # Select distinct sources from DataFrame to be inserted...
    source_df = df[["source", "logo"]]
    source_df = source_df.astype({"source": str})
    source_df = source_df.rename(columns={"source": "name"}).drop_duplicates(
        subset=["name", "logo"]
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


def upsert_new_postings(df: pd.DataFrame, conn: sqlite3.Connection) -> None:
    """Upserts job postings into the postings table with new PK, and links
    to sources and tags table with appropriate FKs.

    Args:
        df (pd.DataFrame): jobs_df from fetch_external_data
        conn (sqlite3.Connection): inject dependency
    """

    # # Inactive old records...
    # db_df = pd.read_sql("SELECT url FROM positions WHERE inactive_date_utc = NULL", conn)
    # db_df = db_df.astype(pd.StringDtype())

    # check_df = df[["url"]].copy()
    # inactivate_df = pd.merge(check_df, db_df, how="outer", indicator=True)
    # check_df = inactivate_df[inactivate_df["_merge"] == "left_only"]

    # inactive_date = datetime.now(timezone.utc)
    # check_df["inactive_date_utc"] = inactive_date
    # check_df = check_df.astype(pd.StringDType())

    # Add the tags FK to the df...
    source_df = pd.read_sql("SELECT id, name FROM sources;", conn)
    source_df["name"] = source_df["name"].astype(pd.StringDtype())

    df = df.rename(columns={"source": "name"})

    print("\t-> Getting [Job].[sources] FKs...")
    df = df.merge(source_df, on="name", how="inner")
    df = df.drop("name", axis=1)
    df = df.rename(columns={"id": "source_id"})

    del source_df

    # Add the tags FK to the df...
    tags_df = pd.read_sql("SELECT id, name FROM tags;", conn)

    print("\t-> Getting [Job].[tags] FKs...")
    df = df.rename(columns={"tags": "name"})
    df = df.merge(tags_df, on="name", how="inner")
    df = df.drop("name", axis=1)
    df = df.rename(columns={"id": "tag_id"})

    del tags_df

    # Add timestamps...
    utc_now = datetime.now(timezone.utc)
    df["active_date_utc"] = utc_now.strftime("%Y-%m-%dT%H:%M:%SZ")
    df["active_date_utc"] = df["active_date_utc"].astype(pd.StringDtype())
    df["inactive_date_utc"] = None
    df["inactive_date_utc"] = df["inactive_date_utc"].astype(pd.StringDtype())

    # Final cleaning of the df
    df = df.drop("logo", axis=1)
    df = df.rename(
        columns={
            "url": "source_url",
            "title": "job_title",
            "date_published": "publish_date",
        }
    )
    df.fillna(value="None", inplace=True)

    # Convert DataFrame to a list of tuples
    postings = df.to_records(index=False).tolist()

    # Prepare the SQL statement
    columns = ", ".join(df.columns)
    placeholders = ", ".join(["?" for _ in df.columns])
    conflict_update = ", ".join(
        [f"{col} = excluded.{col}" for col in df.columns if col != "url"]
    )

    sql = f"""
INSERT INTO postings ({columns})
VALUES ({placeholders})
ON CONFLICT(id) DO UPDATE SET
    {conflict_update}
"""

    # Execute the upsert
    print(f"\t-> Upserting {len(df)} record(s) into [Job].[postings]...")
    cursor = conn.cursor()
    cursor.executemany(sql, postings)
    conn.commit()
    print("db ingestion complete.")
    return


def db_ingestion(df: pd.DataFrame, db_filename: str = "Job.db") -> None:
    """_summary_

    Args:
        df (pd.DataFrame): _description_
        db_filename (str, optional): _description_. Defaults to "Job.db".
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

        print(f"Inserting [{db_filename.split(".")[0]}].[sources] table...")
        insert_new_sources(df, jobs_conn)

        print(f"Inserting [{db_filename.split(".")[0]}].[tags] table...")
        insert_new_tags(df, jobs_conn)

        print(f"Upserting [{db_filename.split(".")[0]}].[postings] table...")
        upsert_new_postings(df, jobs_conn)
    return
