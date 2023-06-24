from typing import List
from fastapi import APIRouter, status, Depends, Form, Query, HTTPException
from fastapi_limiter.depends import RateLimiter
from pydantic import EmailStr

from sqlalchemy.orm import Session

from src.database.models import Client, Roles
from src.schemas.creditcards import AccountNumber, DeactivateCard, CreditCardSearchModel
from src.database.connect import get_db
from src.repository import creditcards as repository_ccards
from src.schemas.creditcards import CreditCardResponseModel
from src.services.roles import RolesChecker


router = APIRouter(prefix="/credit_cards", tags=["credit_cards"])

allowed_create_cards = RolesChecker([Roles.admin, Roles.team_leader])
allowed_update_cards = RolesChecker([Roles.admin, Roles.team_leader, Roles.manager])
allowed_delete_cards = RolesChecker([Roles.admin, Roles.team_leader, Roles.manager])
allowed_get_info = RolesChecker([Roles.admin, Roles.director, Roles.team_leader])


@router.post(
    "/new_credit_card/",
    response_model=CreditCardResponseModel,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(allowed_create_cards),
        Depends(RateLimiter(times=2, seconds=5)),
    ],
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
    dependencies=[
        Depends(allowed_update_cards),
        Depends(RateLimiter(times=2, seconds=5)),
    ],
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


@router.delete(
    "/delete_card/",
    # response_model=CreditCardResponseModel,
    dependencies=[
        Depends(allowed_delete_cards),
        Depends(RateLimiter(times=2, seconds=5)),
    ],
)
async def delete_card(body: DeactivateCard, db: Session = Depends(get_db)):
    check_user_cards = await repository_ccards.check_user_card_repo(body, db)
    if not check_user_cards:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client doesn't have this card or the card doesn't belong to this client",
        )
    card = await repository_ccards.delete_card_repo(body, db)
    return card


@router.get(
    "/active_cards/",
    response_model=List[CreditCardResponseModel],
    dependencies=[
        Depends(allowed_get_info),
        Depends(RateLimiter(times=2, seconds=5)),
    ],
)
async def get_active_cards(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    cards = await repository_ccards.get_active_cards_repo(offset, limit, db)
    if cards:
        return cards
    else:
        return {"detail": "There are no active cards in the DB."}


@router.get(
    "/deactivated_cards/",
    response_model=List[CreditCardResponseModel],
    dependencies=[
        Depends(allowed_get_info),
        Depends(RateLimiter(times=2, seconds=5)),
    ],
)
async def get_deactivated_cards(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    cards = await repository_ccards.get_deactivated_cards_repo(offset, limit, db)
    if cards:
        return cards
    else:
        return {"detail": "There are no active cards in the DB."}
