from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud


def make_fully_invested(objects, iterator):
    objects[iterator].invested_amount = objects[iterator].full_amount
    objects[iterator].fully_invested = True
    objects[iterator].close_date = datetime.now()


async def do_investments(session: AsyncSession):
    charity_projects = await charity_project_crud.get_unfully_invested(session)
    donations = await donation_crud.get_unfully_invested(session)
    if not donations or not charity_projects:
        return
    charity_project_iterator = 0
    donation_iterator = 0
    while (donation_iterator != len(donations) and
           charity_project_iterator != len(charity_projects)):

        charity_project = charity_projects[charity_project_iterator]
        donation = donations[donation_iterator]

        project_remaining_amount = (
            charity_project.full_amount - charity_project.invested_amount
        )
        donation_remaining_amount = (
            donation.full_amount - donation.invested_amount
        )

        if project_remaining_amount > donation_remaining_amount:
            charity_projects[
                charity_project_iterator
            ].invested_amount += donation_remaining_amount

            make_fully_invested(donations, donation_iterator)

            donation_iterator += 1
        elif project_remaining_amount < donation_remaining_amount:
            donations[
                donation_iterator
            ].invested_amount += project_remaining_amount

            make_fully_invested(charity_projects, charity_project_iterator)

            charity_project_iterator += 1
        else:
            make_fully_invested(donations, donation_iterator)
            make_fully_invested(charity_projects, charity_project_iterator)

            charity_project_iterator += 1
            donation_iterator += 1

    session.add_all(donations)
    session.add_all(charity_projects)
    await session.commit()
