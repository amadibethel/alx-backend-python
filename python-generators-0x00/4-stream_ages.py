#!/usr/bin/env python3
"""
Memory-Efficient Aggregation with Generators
"""

import sqlite3

def stream_user_ages():
    """
    Generator that yields user ages one by one
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM users")

    for row in cursor:
        yield row[0]

    conn.close()


def calculate_average_age():
    """
    Calculate the average age without loading entire dataset into memory
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("Average age of users: 0")
    else:
        print(f"Average age of users: {total_age / count:.2f}")


if __name__ == "__main__":
    calculate_average_age()
