from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectDBAllInfo,
                                         CharityProjectIn,
                                         CharityProjectUpdate)
from app.services.investments import do_investments

from .validatords import (check_investment_amount, check_project_exists,
                          check_project_fully_invested,
                          check_project_isnt_invested,
                          check_project_name_unique)

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDBAllInfo],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.post(
    '/',
    response_model=CharityProjectDBAllInfo,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_charity_project(
    obj_in: CharityProjectIn,
    session: AsyncSession = Depends(get_async_session),
):
    await check_project_name_unique(obj_in.name, session)
    new_charity_project = await charity_project_crud.create(obj_in, session)
    await do_investments(session)
    await session.refresh(new_charity_project)
    return new_charity_project


@router.delete(
    '/{project_id}',
    dependencies=[Depends(current_superuser)],
    response_model=CharityProjectDBAllInfo,
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_project_exists(project_id, session)
    await check_project_isnt_invested(project_id, session)
    charity_project = await charity_project_crud.remove(charity_project, session)
    return charity_project


@router.patch(
    '/{project_id}',
    dependencies=[Depends(current_superuser)],
    response_model=CharityProjectDBAllInfo,
)
async def patch_charity_project(
        obj_in: CharityProjectUpdate,
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_project_exists(project_id, session)
    if obj_in.name is not None:
        await check_project_name_unique(obj_in.name, session)
    await check_project_fully_invested(project_id, session)
    if obj_in.full_amount is not None:
        await check_investment_amount(project_id, obj_in.full_amount, session)
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    await do_investments(session)
    await session.refresh(charity_project)
    return charity_project
