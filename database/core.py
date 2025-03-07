import mysql.connector
import mysql.connector.abstracts
import mysql.connector.aio
from contextlib import contextmanager, asynccontextmanager
from typing import Iterator, AsyncIterator


@contextmanager
def get_db(dictionary=True, commit=False) -> Iterator[mysql.connector.abstracts.MySQLCursorAbstract]:
    """
    Context manager for creating a connection to the MySQL database

    Args:
        dictionary (bool): Whether to return the cursor as a dictionary
        commit (bool): Whether to commit the transaction

    Yields:
        (mysql.connector.abstracts.MySQLCursorAbstract): The cursor object to interact with the database
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="bluesky warehouse",
    )
    cursor = conn.cursor(dictionary=dictionary)
    
    yield cursor

    if commit:
        conn.commit()
    cursor.close()
    conn.close()


@asynccontextmanager
async def aget_db(dictionary=True, commit=False) -> AsyncIterator[mysql.connector.aio.abstracts.MySQLCursorAbstract]:
    """
    Async context manager for creating a connection to the MySQL database

    Args:
        dictionary (bool): Whether to return the cursor as a dictionary
        commit (bool): Whether to commit the transaction

    Yields:
        (mysql.connector.aio.abstracts.MySQLCursorAbstract): The cursor object to interact with the database
    """
    async with await mysql.connector.aio.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="bluesky warehouse",
    ) as conn:
        async with await conn.cursor(dictionary=dictionary) as cursor:
            yield cursor
            if commit:
                await conn.commit()
            await cursor.close()
        await conn.close()
