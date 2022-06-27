from typing import Any

import app.util.db as db_util
from app.util.logger import get_logger

_LOG = get_logger(__name__.split(".")[-1])

_SCRIPT = """
CREATE TABLE IF NOT EXISTS object_store (key TEXT PRIMARY KEY, value BLOB);
CREATE TABLE IF NOT EXISTS event_queue (id INT PRIMARY KEY, event TEXT);
"""


async def setup_db() -> Any:
    db = await db_util.connect_file_db()
    await db.executescript(_SCRIPT)
    await db.commit()
    await db.close()


async def db_exists() -> bool:
    try:
        db = await db_util.connect_file_db()
        await db.close()
    except Exception:
        return False
