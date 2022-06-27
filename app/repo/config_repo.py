from app.record.enums import ConfigKey
from app.util import db

_SQL_FETCH_LAST_ID = f"""
SELECT CAST(value as INT) AS last_id FROM object_store 
WHERE key = '{ConfigKey.LAST_ID.value}' LIMIT 1
"""


async def fetch_last_id() -> int:
    raw = await db.fetch_one(_SQL_FETCH_LAST_ID)
    if raw is None or not raw.last_id:
        return 0
    result = raw.get("last_id", 0)
    return result
