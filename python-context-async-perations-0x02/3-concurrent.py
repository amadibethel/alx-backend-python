#!/usr/bin/env python3
"""
Task 2: Concurrent Asynchronous Database Queries
"""

import asyncio
import aiosqlite


async def async_fetch_users():
    """Fetch all users asynchronously"""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("✅ All Users:", results)
            return results


async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously"""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            print("✅ Users Older Than 40:", results)
            return results


async def fetch_concurrently():
    """Run both queries concurrently"""
    results_all, results_older = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results_all, results_older


# Run the concurrent fetch
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
