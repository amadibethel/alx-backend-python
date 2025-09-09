#!/usr/bin/env python3
"""
Task 1: Reusable Query Context Manager
"""

import sqlite3


class ExecuteQuery:
    """Custom context manager to execute a SQL query and return results"""

    def __init__(self, query, params=None, db_name="users.db"):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()


# Example usage
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    with ExecuteQuery(query, params) as results:
        print(" Query Results:", results)
