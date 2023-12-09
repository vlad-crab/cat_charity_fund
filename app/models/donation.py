from sqlalchemy import Column, ForeignKey, Integer, Text

from .charity_donation_base import CharityDonationBase
from app.core.db import Base


class Donation(Base, CharityDonationBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
