#!/usr/bin/python3
"""
Lazy pagination with Python generators.

- paginate_users(page_size, offset): fetch a single page from user_data table
- lazy_pagination(page_size): lazily yields each page using a generator
"""

import seed


def paginate_users(page_size, offset):
    """
    Fetch a single page of users from the database.

    Args:
        page_size (int): number of rows per page
        offset (int): starting row offset

    Returns:
        list of dict: rows fetched from the table
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily fetches pages of users from user_data table.

    Args:
        page_size (int): number of rows per page

    Yields:
        list of dict: one page of users at a time
    """
    offset = 0
    while True:  # only one loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
