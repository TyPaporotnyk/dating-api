from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


def get_datetime_utc_now() -> datetime:
    datetime_now = datetime.now(tz=timezone.utc)
    return datetime_now.replace(tzinfo=None)


class TimeStampMinix:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=get_datetime_utc_now, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=get_datetime_utc_now,
        onupdate=get_datetime_utc_now,
        server_default=func.now(),
        server_onupdate=func.now(),
    )


class UUIDMixin:
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, unique=True)
