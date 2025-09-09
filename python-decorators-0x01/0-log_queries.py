#!/usr/bin/env python3
"""
Task 0: Logging database queries with a decorator
"""

import sqlite3
import functools


def log_queries(func):
    """Decorator to log SQL queries before executing them"""
    @functools.wraps(func)
    def wrapper(query, *args, **kwargs):
        print(f"Executing SQL Query: {query}")
        return func(query, *args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    """Fetch all users from the users table"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Example usage (will log the query before running it)
if __name__ == "__main__":
    users = fetch_all_users("SELECT * FROM users")
    print(users)
