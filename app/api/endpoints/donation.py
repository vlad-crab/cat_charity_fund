from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.schemas.donation import DonationDBAllInfo, DonationDB, DonationCreate
from app.services.investments import do_investments

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDBAllInfo],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=list[DonationDB]
)
async def get_my_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    donations = await donation_crud.get_all_users_donations(user.id, session)
    return donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_donation(
    obj_in: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    donation = await donation_crud.create(obj_in, session, user)
    await do_investments(session)
    await session.refresh(donation)
    return donation
