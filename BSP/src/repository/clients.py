# For testing
import os
import sys

sys.path.append(os.path.abspath("."))


from fastapi import Depends

from sqlalchemy.orm import Session
from src.database.models import Client, Account
from src.schemas.clients import ClientModel, UpdateVIPClientModel
from src.database.connect import get_db

# For testing
from src.database.connect import session


async def create_client(body: ClientModel, sex: str, db: Session) -> Client:
    body_dict = body.dict()
    body_dict["sex"] = sex
    new_client = Client(**body_dict)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


async def check_existing_client_by_tax_number(tax_number: str, db: Session) -> Client:
    client = db.query(Client).filter_by(tax_number=int(tax_number)).first()
    return client


# async def check_existing_client_by_email(email: str, db: Session) -> Client:
#     client = db.query(Client).filter_by(email=email).first()
#     return client


async def get_clients_accounts(client_id: int, db: Session) -> list:
    accounts = db.query(Account).filter_by(client_id=client_id).all()
    return accounts


async def get_all_active_clients_repo(db: Session, limit: int, offset: int) -> list:
    clients = db.query(Client).filter_by(active=True).limit(limit).offset(offset).all()
    return clients


async def get_all_unactive_clients_repo(db: Session, limit: int, offset: int) -> list:
    clients = db.query(Client).filter_by(active=False).limit(limit).offset(offset).all()
    return clients


async def get_all_vip_clients_repo(db: Session, limit: int, offset: int) -> list:
    clients = (
        db.query(Client)
        .filter_by(vip=True, active=True)
        .limit(limit)
        .offset(offset)
        .all()
    )
    return clients


async def get_all_non_vip_clients_repo(db: Session, limit: int, offset: int) -> list:
    clients = (
        db.query(Client)
        .filter_by(vip=False, active=True)
        .order_by(Client.id)
        .limit(limit)
        .offset(offset)
        .all()
    )
    return clients


async def update_vip_status_repo(body: UpdateVIPClientModel, status: str, db: Session):
    new_status = None
    client = db.query(Client).filter_by(tax_number=int(body.tax_number)).first()

    if status == "true":
        new_status = True
    if status == "false":
        new_status = False
    if client:
        client.vip = new_status
        db.commit()

    return client

    # db.query(Client)
    # .filter_by(vip=False, active=True)
    # .order_by(Client.first_name.desc())
    # .limit(limit)
    # .offset(offset)
    # .all()
