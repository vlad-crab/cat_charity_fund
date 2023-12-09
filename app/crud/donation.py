from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .base import CRUDBase
from app.models.donation import Donation


class DonationCRUD(CRUDBase):

    async def get_all_users_donations(
        self,
        user_id,
        session: AsyncSession
    ) -> list[Donation]:
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user_id)
        )
        donations = donations.scalars().all()
        return donations


donation_crud = DonationCRUD(Donation)
