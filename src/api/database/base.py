from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

# Import all models here to ensure they are registered with Base
# For example:
from src.api.models.user import User # noqa
# from app.models.item import Item # noqa

__all__ = ["User"]  