"""
CNCS Chatbot - Database Layer
Responsible only for opening connections and executing queries.
"""

import sqlite3
from config import DATABASE_NAME


def get_db():
    """Create a database connection with row factory."""
    db = sqlite3.connect(DATABASE_NAME)
    db.row_factory = sqlite3.Row
    return db


def query_db(sql, params=""):
    """Execute a SQL query and return all results."""
    db = get_db()
    cursor = db.cursor()

    if params:
        cursor.execute(sql, (params,))
    else:
        cursor.execute(sql)

    data = cursor.fetchall()
    db.close()
    return data
