#!/usr/bin/python3
"""
Generator that streams rows from the user_data table in the ALX_prodev database.
"""

import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    Generator function to stream rows one by one from the user_data table.
    Yields each row as a dictionary.
    """
    try:
        # Connect directly to ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # 🔴 Replace with your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        # Use a single loop and yield rows
        for row in cursor:
            yield row

    except Error as e:
        print(f"Error streaming users: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
