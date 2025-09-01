#!/usr/bin/python3
"""
Batch processing with Python generators.

- stream_users_in_batches(batch_size): yields rows from the user_data table in batches
- batch_processing(batch_size): yields users over age 25 from each batch
"""

import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows in batches from the user_data table.

    Args:
        batch_size (int): number of rows per batch

    Yields:
        list of dict: batch of users
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # Replace with your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch  # yield one batch at a time

    except Error as e:
        print(f"Error fetching batches: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def batch_processing(batch_size):
    """
    Generator that processes batches and yields users over age 25.

    Args:
        batch_size (int): number of rows per batch

    Yields:
        dict: user row where age > 25
    """
    for batch in stream_users_in_batches(batch_size):  # loop #1
        for user in batch:  # loop #2
            if int(user["age"]) > 25:
                yield user  # use yield instead of print/return
