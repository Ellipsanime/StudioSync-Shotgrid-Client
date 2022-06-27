from datetime import datetime, timedelta
from typing import Any, List, Dict, Union, Iterator, Optional

from box import Box

from app.util.logger import get_logger
from app.util.shotgrid import shotgrid

_LOG = get_logger(__name__.split(".")[-1])

_LIMIT = 500
_TYPE = "EventLogEntry"
_ORDER = [{"column": "created_at", "direction": "asc"}]
_FIELDS = [
    "id",
    "event_type",
    "attribute_name",
    "meta",
    "entity",
    "user",
    "project",
    "session_uuid",
    "created_at",
]
_FILTERS = [
    {
        "filter_operator": "all",
        "filters": [
            ["project", "is_not", None],
            ["entity", "is_not", None],
        ],
    }
]
_IGNORED_EVENT_TYPE = {"Shotgun_Attachment_View"}


def _filters_with_id(last_id: int) -> List[Dict[str, Any]]:
    return [
        *_FILTERS,
        {
            "filter_operator": "all",
            "filters": [["id", "greater_than", last_id]],
        },
    ]


def _post_filter_events(events: List[Box]) -> Iterator[Box]:
    for x in events:
        if x.get("event_type") in _IGNORED_EVENT_TYPE:
            continue
        yield x


def _fetch_events(
    filters: List[Union[List[Any], Dict[str, str]]]
) -> List[Box]:
    client = shotgrid()
    raw_events = client.find(_TYPE, filters, _FIELDS, _ORDER, _LIMIT)
    return list(_post_filter_events(raw_events))


def find_latest_events_by_id(last_id: int) -> List[Box]:
    _LOG.info(f"find latest events with id: {last_id}")
    return _fetch_events(_filters_with_id(last_id))
