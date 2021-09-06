from sqlalchemy import Column, DateTime, String

from app.models import Base
from app.models.mixins.id import IdModel


class Link(Base, IdModel):
    __tablename__ = "link"

    description = Column(String, nullable=False)
    date_opened = Column(DateTime)

    @property
    def url(self):
        return f"http://project4473614.tilda.ws?_ltid={self.id}"
