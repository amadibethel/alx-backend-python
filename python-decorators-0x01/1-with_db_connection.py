#!/usr/bin/env python3
"""
Task 1: Handle Database Connections with a Decorator
"""

import sqlite3
import functools


def with_db_connection(func):
    """Decorator to handle opening and closing of database connection"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            # Pass the connection to the decorated function
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    """Fetch user by ID from users table"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Example usage (fetch user with ID = 1)
if __name__ == "__main__":
    user = get_user_by_id(user_id=1)
    print(user)
