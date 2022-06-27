from typing import Any

import jsonpickle
from box import Box
from returns.future import future_safe

from app.util import db
from app.util.logger import get_logger

_LOG = get_logger(__name__.split(".")[-1])

_SQL_PUT_EVENT = """
REPLACE INTO event_queue (id, event) VALUES (?, ?)
"""


@future_safe
async def upsert_event(event_id: int, event: Box) -> Any:
    return await db.write_data(
        _SQL_PUT_EVENT,
        (event_id, jsonpickle.dumps(event)),
    )

