# For testing
import os
import sys

sys.path.append(os.path.abspath("."))


from fastapi import Depends

from sqlalchemy.orm import Session
from src.database.models import Client, Account, Manager
from src.schemas.managers import ManagerModel, ChangeRoleModel
from src.database.connect import get_db

# For testing
from src.database.connect import session


async def check_existing_manager_by_email(email: str, db: Session) -> bool:
    manager = db.query(Manager).filter_by(email=email).first()
    return manager


async def create_manager_repo(body: ManagerModel, db: Session) -> Manager:
    new_manager = Manager(**body.dict())
    db.add(new_manager)
    db.commit()
    db.refresh(new_manager)
    return new_manager


async def change_role_repo(body: ChangeRoleModel, role: str, db: Session):
    manager = db.query(Manager).filter_by(email=body.email).first()
    manager.roles = role
    db.commit()

    return manager


async def remove_manager_repo(body: ChangeRoleModel, db: Session):
    manager = db.query(Manager).filter_by(email=body.email).first()
    db.delete(manager)
    db.commit()
    return {"detail": "Manager was removed from DB successfully."}


async def update_token_repo(manager: ManagerModel, refesh_token: str, db: Session):
    manager.refresh_token = refesh_token
    db.commit()