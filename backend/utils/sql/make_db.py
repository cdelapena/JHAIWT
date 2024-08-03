import sqlite3


def init_tables(conn: sqlite3.Connection) -> None:
    """Initialize Job.db tables

    Args:
        conn (sqlite3.Connection): inject dependencies
    """
    # Ensure FKs are enforced...
    conn.execute("PRAGMA foreign_keys = 1")

    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS postings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    company_name TEXT,
    title TEXT,
    description TEXT,
    preprocessed_description TEXT,
    candidate_required_location TEXT,
    job_type TEXT,
    url TEXT,
    salary TEXT,
    publish_date TEXT,
    active_date_utc TEXT,
    inactive_date_utc TEXT,
    FOREIGN KEY (source_id) REFERENCES sources (id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE SET NULL ON UPDATE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS postingtags (
    posting_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (posting_id, tag_id),
    FOREIGN KEY (posting_id) REFERENCES postings (id),
    FOREIGN KEY (tag_id) REFERENCES tags (id)
    )
    """)

    return
