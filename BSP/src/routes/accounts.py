from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.models import Roles
from src.database.connect import get_db
from src.schemas.accounts import (
    AccountResponseModel,
    AccountModel,
    ToDepositCash,
    CurrentDepositResponseModel,
    DeactivateAccountdModel,
    TopAccountsModel,
)
from src.repository import accounts as repository_accounts
from src.repository import clients as repository_clients
from src.services.roles import RolesChecker

router = APIRouter(prefix="/accounts", tags=["accounts"])

allowed_create_accounts = RolesChecker([Roles.admin, Roles.team_leader])
allowed_update_accounts = RolesChecker([Roles.admin, Roles.team_leader, Roles.manager])
allowed_delete_accounts = RolesChecker([Roles.admin, Roles.team_leader])
allowed_get_info = RolesChecker([Roles.admin, Roles.team_leader, Roles.director])


@router.post(
    "/",
    response_model=AccountResponseModel,
    name="Create account",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(allowed_create_accounts),
        # Depends(RateLimiter(times=2, seconds=5)),
    ],
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
    name="Deposit cash",
    dependencies=[
        Depends(allowed_update_accounts),
        # Depends(RateLimiter(times=2, seconds=5)),
    ],
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
    account = await repository_accounts.deposit_cash_repo(body, db)
    return account


@router.patch(
    "/withdraw_cash/",
    response_model=CurrentDepositResponseModel,
    name="Withdraw cash",
    dependencies=[
        Depends(allowed_update_accounts),
        # Depends(RateLimiter(times=2, seconds=5)),
    ],
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


@router.patch(
    "/deactivate_account/",
    response_model=AccountResponseModel,
    name="Deactivate account",
    dependencies=[
        Depends(allowed_delete_accounts),
        # Depends(RateLimiter(times=2, seconds=5)),
    ],
)
async def deactivate_account(
    body: DeactivateAccountdModel, db: Session = Depends(get_db)
):
    account = await repository_accounts.check_account_exists(body.account_number, db)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found."
        )
    deactivated_account = await repository_accounts.deactivate_account_repo(account, db)
    return deactivated_account


@router.get(
    "/top_five_accounts/",
    response_model=List[TopAccountsModel],
    name="Top 5 accounts",
    dependencies=[
        Depends(allowed_get_info),
        # Depends(RateLimiter(times=2, seconds=5)),
    ],
)
async def get_top_five_accounts(db: Session = Depends(get_db)):
    accounts = await repository_accounts.get_top_five_accounts_repo(db)
    result = await repository_accounts.convert_top_five_to_dict(accounts)
    return result


@router.delete(
    "/delete_account/",
    name="Delete account",
    dependencies=[
        Depends(allowed_delete_accounts),
        # Depends(RateLimiter(times=2, seconds=5)),
    ],
)
async def delete_account(
    body: DeactivateAccountdModel,
    db: Session = Depends(get_db),
):
    account = await repository_accounts.check_account_exists(body.account_number, db)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found."
        )
    deactivated_account = await repository_accounts.delete_account_repo(account, db)
    return deactivated_account
