from typing import Any

from app.repo import config_repo
from app.util.logger import get_logger

_LOG = get_logger(__name__.split(".")[-1])


async def synchronize_all() -> Any:
    _LOG.info("Fetching last event id...")
    _LOG.debug(await config_repo.fetch_last_id())

