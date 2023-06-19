# For testing
import os
import sys
import random

sys.path.append(os.path.abspath("."))


from fastapi import Depends

from sqlalchemy.orm import Session
from src.database.models import Account, Client
from src.schemas.accounts import AccountModel
from src.database.connect import get_db

# For testing
from src.database.connect import session


async def create_unique_acc_number():
    return f"GB{random.randrange(1000000, 99999999999999)}"


async def create_account_repo(client: Client, db: Session):
    accounts = [acc.account_number for acc in db.query(Account).all()]
    new_account_number = await create_unique_acc_number()
    while True:
        if new_account_number not in accounts:
            break
        else:
            new_account_number = await create_unique_acc_number()

    new_account = Account(account_number=new_account_number, client_id=client.id)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account
