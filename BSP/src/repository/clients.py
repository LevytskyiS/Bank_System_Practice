from fastapi import Depends

from sqlalchemy.orm import Session
from src.database.models import Client
from src.schemas.clients import ClientModel
from src.database.connect import get_db


async def create_client(body: ClientModel, db: Session):
    new_user = Client(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
