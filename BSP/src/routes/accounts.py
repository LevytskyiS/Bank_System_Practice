from typing import List
from fastapi import APIRouter, status, Depends, Form, Query, HTTPException
from fastapi_limiter.depends import RateLimiter
from pydantic import EmailStr

from sqlalchemy.orm import Session

from src.database.models import Client
from src.schemas.accounts import (
    AccountResponseModel,
    AccountModel,
    ToDepositCash,
    CurrentDepositResponseModel,
)
from src.database.connect import get_db
from src.repository import accounts as repository_accounts
from src.repository import clients as repository_clients

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post(
    "/",
    response_model=AccountResponseModel,
    name="Create account",
    status_code=status.HTTP_201_CREATED,
    # dependencies=[
    # Depends(allowed_create_users),
    # Depends(RateLimiter(times=2, seconds=5)),
    # ],
)
async def create_account(
    body: AccountModel,
    db: Session = Depends(get_db),
):
    client = await repository_clients.check_existing_client_by_tax_number(
        body.tax_number, db
    )
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found."
        )
    account = await repository_accounts.create_account_repo(client, db)
    return account


@router.patch(
    "/deposit_cash/",
    response_model=CurrentDepositResponseModel,
    name="Deposit cash"
    # dependencies=[
    # Depends(allowed_create_users),
    # Depends(RateLimiter(times=2, seconds=5)),
    # ],
)
async def deposit_cash(
    body: ToDepositCash,
    db: Session = Depends(get_db),
):
    check_account = await repository_accounts.check_account_exists(
        body.account_number, db
    )
    if not check_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found."
        )
    account = await repository_accounts.deposit_cash_repo(body, check_account, db)
    return account


@router.patch(
    "/withdraw_cash/",
    response_model=CurrentDepositResponseModel,
    name="Deposit cash"
    # dependencies=[
    # Depends(allowed_create_users),
    # Depends(RateLimiter(times=2, seconds=5)),
    # ],
)
async def withdraw_cash(
    body: ToDepositCash,
    db: Session = Depends(get_db),
):
    check_account = await repository_accounts.check_account_exists(
        body.account_number, db
    )
    if not check_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found."
        )
    account = await repository_accounts.withdraw_cash_repo(body, check_account, db)
    return account
