from app.models.charity_project import CharityProject

from .base import CRUDBase


class CharityProjectCRUD(CRUDBase):
    pass


charity_project_crud = CharityProjectCRUD(CharityProject)
