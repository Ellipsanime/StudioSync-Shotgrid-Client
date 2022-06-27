from typing import Any

from returns.future import future_safe

from app.record.enums import ConfigKey
from app.util import db
from app.util.logger import get_logger

_LOG = get_logger(__name__.split(".")[-1])

_SQL_REPLACE_LAST_ID = """
REPLACE INTO object_store (key, value) VALUES (?, ?)
"""


@future_safe
async def write_last_event_id(last_id: int) -> Any:
    return await db.write_data(
        _SQL_REPLACE_LAST_ID,
        (ConfigKey.LAST_ID.value, last_id),
    )
