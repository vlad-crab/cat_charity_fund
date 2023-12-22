from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base

from .charity_donation_base import CharityDonationBase


class Donation(Base, CharityDonationBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
