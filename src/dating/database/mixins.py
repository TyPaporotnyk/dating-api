from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from dating.utils.datetime import get_datetime_utc_now


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
