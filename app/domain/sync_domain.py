import os
from typing import Any

from app.repo import config_repo, shotgrid_event_repo
from app.util.logger import get_logger

_LOG = get_logger(__name__.split(".")[-1])
_MIN_LAST_ID = os.environ.get("MIN_LAST_ID", 0)


async def synchronize_all() -> Any:
    _LOG.info("Fetching last event id...")
    last_id = max(await config_repo.fetch_last_id(), _MIN_LAST_ID)
    shotgrid_event_repo.find_latest_events_by_id(last_id)

    _LOG.info("Fetching events...")

