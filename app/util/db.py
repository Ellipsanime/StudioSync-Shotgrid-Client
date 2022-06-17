import os
from typing import Tuple, List, Any

import aiosqlite
from aiosqlite import Connection, Cursor
from box import Box

from app.util.data import boxify
from app.util.logger import get_logger

_LOG = get_logger(__name__.split(".")[-1])


async def connect_file_db(flag: str = "rwc") -> Connection | None:
    try:
        db_path = os.environ["DB_PATH"]
        db = await aiosqlite.connect(f"file:{db_path}?mode={flag}", uri=True)
        await db.set_trace_callback(_LOG.debug)
        cursor = await db.execute("PRAGMA foreign_keys = 1;")
        await cursor.close()
        db.row_factory = aiosqlite.Row
        return db
    except Exception as ex:
        _LOG.error(ex)
        return None


async def write_data(
    query: str,
    params: Tuple | None = None,
) -> Box:

    db = await connect_file_db()
    if not db:
        raise Exception("Unable to connect the db")
    try:
        cursor = await db.execute(query, params)
        result = boxify(
            {"row_count": cursor.rowcount, "row_id": cursor.lastrowid}
        )

        await db.commit()
        await cursor.close()

        return result
    except Exception as ex:
        _LOG.exception(ex)
        raise ex
    finally:
        if db:
            await db.close()


async def fetch_one(
    query: str,
    params: Tuple | None = None,
) -> Box | None:

    db = await connect_file_db()
    if not db:
        raise Exception("Unable to connect the db")

    try:
        cursor = await db.execute(query, params)
        row = await cursor.fetchone()
        if row is None:
            return row
        result = boxify(dict(zip(row.keys(), row)))

        await cursor.close()

        return result
    except Exception as ex:
        _LOG.exception(ex)
        raise ex
    finally:
        if db:
            await db.close()


async def fetch_all(
    query: str,
    params: Tuple | None = None,
) -> List[Box]:
    
    db = await connect_file_db()
    if not db:
        raise Exception("Unable to connect the db")
    try:
        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()
        if rows is None:
            return []
        result = [boxify(dict(zip(x.keys(), x))) for x in rows]

        await cursor.close()

        return result
    except Exception as ex:
        _LOG.exception(ex)
        raise ex
    finally:
        if db:
            await db.close()
