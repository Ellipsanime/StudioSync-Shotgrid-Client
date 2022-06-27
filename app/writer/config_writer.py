


def write_last_event_id(last_id: int) -> Any:
    return storage.write_object(LAST_ID_KEY, last_id)