#!/usr/bin/env python3
"""
Task 3: Retry Database Queries
"""

import time
import sqlite3
import functools


def with_db_connection(func):
    """Decorator to handle opening and closing of database connection"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def retry_on_failure(retries=3, delay=2):
    """Decorator to retry a function on failure"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"⚠️ Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
            # If all retries fail, raise the last exception
            raise last_exception
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """Fetch all users from the database, retrying on failure"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# Example usage
if __name__ == "__main__":
    try:
        users = fetch_users_with_retry()
        print("Users fetched successfully:", users)
    except Exception as e:
        print("❌ Failed after retries:", e)
