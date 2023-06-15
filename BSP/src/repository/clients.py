# For testing
import os
import sys

sys.path.append(os.path.abspath("."))


from fastapi import Depends

from sqlalchemy.orm import Session
from src.database.models import Client
from src.schemas.clients import ClientModel
from src.database.connect import get_db

# For testing
from src.database.connect import session


async def create_client(body: ClientModel, sex: str, db: Session):
    body_dict = body.dict()
    body_dict["sex"] = sex
    new_user = Client(**body_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def check_existing_client_by_email(email: str, db: Session):
    client = db.query(Client).filter_by(email=email).first()
    return client
