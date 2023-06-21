# For testing
import os
import sys
import random

sys.path.append(os.path.abspath("."))


from fastapi import Depends

from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from src.database.models import Account, Client, CreditCard
from src.schemas.accounts import AccountModel, ToDepositCash
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


async def check_account_exists(account_number: str, db: Session):
    account = db.query(Account).filter_by(account_number=account_number).first()
    return account


async def deposit_cash_repo(body: ToDepositCash, db: Session):
    account = db.query(Account).filter_by(account_number=body.account_number).first()
    account.current_deposit += int(body.amount)
    db.commit()
    return account


async def withdraw_cash_repo(body: ToDepositCash, account: Account, db: Session):
    account.current_deposit -= int(body.amount)
    db.commit()
    return account


async def deactivate_account_repo(account: Account, db: Session):
    account.active = False
    db.commit()
    return account


async def get_top_five_accounts_repo(db: Session):
    accounts = (
        db.query(
            Client.id,
            Account.current_deposit,
            Account.account_number,
        )
        .select_from(Client)
        .join(Account)
        .order_by(desc(Account.current_deposit))
        .limit(5)
        .all()
    )
    return accounts


async def convert_top_five_to_dict(accounts: list) -> list:
    result = []
    for a in accounts:
        account = {
            "client_id": a[0],
            "current_deposit": a[1],
            "account_number": a[2],
        }
        result.append(account)
    return result
