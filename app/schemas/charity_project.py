from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, Field, Extra


class CharityProjectBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    full_amount: PositiveInt
    description: str = Field(min_length=1)


class CharityProjectDBAllInfo(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectIn(CharityProjectBase):
    pass


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(min_length=1, max_length=100)
    full_amount: Optional[PositiveInt] = None
    description: Optional[str] = Field(min_length=1)

    class Config:
        extra = Extra.forbid
