from .base import CRUDBase
from app.models.charity_project import CharityProject


class CharityProjectCRUD(CRUDBase):
    pass


charity_project_crud = CharityProjectCRUD(CharityProject)
