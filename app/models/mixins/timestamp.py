"""Mixin for `created_date` and `updated_date`."""

from datetime import datetime

from sqlalchemy import Column, DateTime


class TimestampModel:
    created_date = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)
    updated_date = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        index=True,
        nullable=False,
    )
