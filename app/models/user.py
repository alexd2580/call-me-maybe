from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.mutable import MutableDict

from app.models import Base
from app.models.mixins.id import IdModel
from app.models.mixins.timestamp import TimestampModel


class User(Base, IdModel, TimestampModel):
    __tablename__ = "user"

    email = Column(String(100), nullable=False, index=True, unique=True)

    # Oauth2 setup for access to google sheets.
    oauth2_state = Column(String(100))
    oauth2_credentials = Column(MutableDict.as_mutable(JSON))

    # Spreadsheet config.
    source_domain = Column(String(100))
    spreadsheet_id = Column(String(100))
    sheet_name = Column(String(100))
    match_column = Column(String(3))
    date_column = Column(String(3))
