# For testing
import os
import sys
import random

sys.path.append(os.path.abspath("."))


from fastapi import Depends

from sqlalchemy.orm import Session
from src.database.models import Account, CreditCard, Client
from src.schemas.clients import ClientModel, UpdateVIPClientModel
from src.schemas.creditcards import DeactivateCard
from src.database.connect import get_db


# For testing
from src.database.connect import session


async def create_unique_card_number():
    return random.randrange(100000, 999999999)


async def check_existing_account_repo(account_id: int, db: Session):
    account = db.query(Account).filter_by(id=account_id).first()
    return account


async def create_credit_card_repo(account_id: int, db: Session):
    card_number = await create_unique_card_number()
    card_numbers_db = [cc.card_number for cc in db.query(CreditCard).all()]
    while True:
        if card_number not in card_numbers_db:
            break
        else:
            card_number = await create_unique_card_number()
    new_credit_card = CreditCard(
        card_number=card_number, pin_code=1111, account_id=account_id
    )
    db.add(new_credit_card)
    db.commit()
    db.refresh(new_credit_card)
    return new_credit_card


async def check_user_card_repo(body: DeactivateCard, db: Session):
    user_cards = (
        db.query(Client.tax_number, CreditCard.card_number)
        .select_from(Client)
        .join(Account)
        .join(CreditCard)
        .filter(Client.tax_number == int(body.client_tax_number))
        .all()
    )
    if user_cards and int(body.card_number) in [c[1] for c in user_cards]:
        return True
    else:
        return False


async def deactivate_card_repo(body: DeactivateCard, db: Session):
    card = db.query(CreditCard).filter_by(card_number=int(body.card_number)).first()
    card.activated = False
    db.commit()
    return card


async def delete_card_repo(body: DeactivateCard, db: Session):
    card = db.query(CreditCard).filter_by(card_number=int(body.card_number)).first()
    db.delete(card)
    db.commit()
    return {"detaile": "The credit card has been removed from DB successfully."}
