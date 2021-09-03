import uuid

from sqlalchemy import Column, String, DateTime

from app.models import Base


class Link(Base):
    __tablename__ = "link"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    description = Column(String, nullable=False)
    date_opened = Column(DateTime)

    @property
    def url(self):
        return f"http://project4473614.tilda.ws?_ltid={self.id}"
