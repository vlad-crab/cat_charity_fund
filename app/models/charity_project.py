from sqlalchemy import Column, String, Text

from app.core.db import Base

from .charity_donation_base import CharityDonationBase


class CharityProject(Base, CharityDonationBase):
    name = Column(String(100), unique=True)
    description = Column(Text, nullable=False)
