"""
Database utilities for Education Intelligence System
"""

import sqlite3
from pathlib import Path
from config import settings
from .logger import setup_logger

logger = setup_logger(__name__)


def get_db_connection():
    """
    Get database connection

    Returns:
        sqlite3 connection object
    """
    try:
        db_path = Path(settings.DB_FILE)
        connection = sqlite3.connect(str(db_path))
        connection.row_factory = sqlite3.Row
        logger.info(f"Connected to database: {db_path}")
        return connection
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise


def close_db_connection(connection):
    """
    Close database connection safely

    Args:
        connection: sqlite3 connection object
    """
    if connection:
        connection.close()
        logger.info("Database connection closed")


def execute_query(query: str, params: tuple = None):
    """
    Execute a database query

    Args:
        query: SQL query string
        params: Query parameters

    Returns:
        Query results
    """
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        if params:
            result = cursor.execute(query, params).fetchall()
        else:
            result = cursor.execute(query).fetchall()
        connection.commit()
        return result
    except Exception as e:
        logger.error(f"Query execution error: {e}")
        connection.rollback()
        raise
    finally:
        close_db_connection(connection)
