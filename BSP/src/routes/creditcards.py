from typing import List
from fastapi import APIRouter, status, Depends, Form, Query, HTTPException
from fastapi_limiter.depends import RateLimiter
from pydantic import EmailStr

from sqlalchemy.orm import Session

from src.database.models import Client
from src.schemas.creditcards import AccountNumber, DeactivateCard
from src.database.connect import get_db
from src.repository import creditcards as repository_ccards
from src.schemas.creditcards import CreditCardResponseModel


router = APIRouter(prefix="/credit_cards", tags=["credit_cards"])


@router.post(
    "/new_credit_card/",
    response_model=CreditCardResponseModel,
    status_code=status.HTTP_201_CREATED,
    # dependencies=[
    # Depends(allowed_create_users),
    # Depends(RateLimiter(times=2, seconds=5)),
    # ],
)
async def create_credit_card(body: AccountNumber, db: Session = Depends(get_db)):
    account = await repository_ccards.check_existing_account_repo(
        int(body.account_id), db
    )
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found."
        )
    credit_card = await repository_ccards.create_credit_card_repo(account.id, db)
    return credit_card


@router.post(
    "/deactivate_card/",
    response_model=CreditCardResponseModel,
    # Depends(allowed_create_users),
    # Depends(RateLimiter(times=2, seconds=5)),
    # ],
)
async def deactivate_card(body: DeactivateCard, db: Session = Depends(get_db)):
    check_user_cards = await repository_ccards.check_user_card_repo(body, db)
    if not check_user_cards:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client doesn't have this card or the card doesn't belong to this client",
        )
    card = await repository_ccards.deactivate_card_repo(body, db)
    return card
