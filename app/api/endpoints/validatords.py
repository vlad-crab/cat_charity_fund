from fastapi import HTTPException

from app.crud.charity_project import charity_project_crud


async def check_project_name_unique(
    project_name, session
):
    charity_project = await charity_project_crud.get_by_attribute(
        attr_name='name',
        attr_value=project_name,
        session=session,
    )
    if charity_project:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )


async def check_project_exists(project_id, session):
    charity_project = await charity_project_crud.get(
        project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Project with this id doesnt exist'
        )
    return charity_project


async def check_project_isnt_invested(project_id, session):
    charity_project = await charity_project_crud.get(
        project_id, session
    )
    if charity_project.invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    if charity_project.close_date is not None:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_investment_amount(project_id, new_full_amount, session):
    charity_project = await charity_project_crud.get(
        project_id, session
    )
    if charity_project.invested_amount > new_full_amount:
        raise HTTPException(
            status_code=422,
            detail=f'{charity_project.invested_amount} already invested, cant change to lower than this'
        )


async def check_project_fully_invested(project_id, session):
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project.fully_invested or \
            charity_project.invested_amount == charity_project.full_amount:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )
