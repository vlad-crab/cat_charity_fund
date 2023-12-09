from sqlalchemy import Column, String, Text

from .charity_donation_base import CharityDonationBase

from app.core.db import Base


class CharityProject(Base, CharityDonationBase):
    name = Column(String(100), unique=True)
    description = Column(Text, nullable=False)
