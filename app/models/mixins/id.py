"""Model mixin for `id`."""
import uuid

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID


class IdModel:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    #
    # @classmethod
    # def get(cls, id: uuid.UUID):
    #     entity = cls.query.get(id)
    #     if not entity:
    #         raise NotFound(f"{cls.__tablename__} {id} not found")
    #     return entity
