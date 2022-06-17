from app.util import db

LAST_ID_KEY = 'shotgrid.events.last_id'

_SQL_FETCH_LAST_ID = f"""
SELECT CAST(value as INT) FROM object_store 
WHERE key = '{LAST_ID_KEY}' LIMIT 1
"""


async def fetch_last_id() -> int:
    raw = await db.fetch_one(_SQL_FETCH_LAST_ID)
    if raw is None:
        return 0
    result = raw.get(LAST_ID_KEY, 0)
    return result
