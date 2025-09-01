#!/usr/bin/python3
"""
Seed script for setting up the MySQL database ALX_prodev,
creating user_data table, and inserting data from CSV.
"""

import mysql.connector
from mysql.connector import Error
import csv
import uuid


def connect_db():
    """Connects to the MySQL server (without selecting a database)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password"  # 🔴 Replace with your MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    return None


def create_database(connection):
    """Creates the database ALX_prodev if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created successfully (or already exists)")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()


def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # 🔴 Replace with your MySQL password
            database="ALX_prodev"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
    return None


def create_table(connection):
    """Creates the user_data table if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX(user_id)
            );
        """)
        connection.commit()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()


def insert_data(connection, csv_file):
    """Inserts data from CSV into the user_data table (skipping duplicates)."""
    try:
        cursor = connection.cursor()
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = row["age"]

                cursor.execute("""
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s);
                """, (user_id, name, email, age))
        connection.commit()
        print("Data inserted successfully")
    except Error as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
