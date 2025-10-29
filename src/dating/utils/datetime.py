from datetime import UTC, datetime


def get_datetime_utc_now() -> datetime:
    datetime_now = datetime.now(tz=UTC)
    return datetime_now.replace(tzinfo=None)
