from typing import Optional
from pydantic import BaseModel


class NewLink(BaseModel):
    description: str
    url: Optional[str]

    class Config:
        orm_mode = True
