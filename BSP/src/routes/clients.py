from typing import List
from fastapi import APIRouter, status, Depends, Form, Query, HTTPException
from fastapi_limiter.depends import RateLimiter
from pydantic import EmailStr

from sqlalchemy.orm import Session

from src.database.models import Client
from src.schemas.clients import (
    ClientModel,
    ResponseClientModel,
    UpdateVIPClientModel,
    VIPStatusResponse,
)
from src.database.connect import get_db
from src.repository import clients as repository_clients

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post(
    "/",
    response_model=ResponseClientModel,
    name="Create client",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        # Depends(allowed_create_users),
        # Depends(RateLimiter(times=2, seconds=5)),
    ],
)
async def create_client(
    body: ClientModel,
    db: Session = Depends(get_db),
    sex=Query(enum=["male", "female"]),
):
    check_tax_number = await repository_clients.check_existing_client_by_tax_number(
        body.tax_number, db
    )
    if check_tax_number:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Client with such TN is already registered",
        )
    client = await repository_clients.create_client(body, sex, db)
    # body.password = auth_service.get_password_hash(body.password)
    # user = await repository_users.create_user(body, db)
    return client


@router.get(
    "/client/",
    response_model=ResponseClientModel,
    name="Get client",
    # dependencies=[
    #     Depends(allowed_create_users),
    #     Depends(RateLimiter(times=2, seconds=5)),
    # ],
)
async def get_one_client(tax_number: int, db: Session = Depends(get_db)):
    client = await repository_clients.check_existing_client_by_tax_number(
        tax_number, db
    )
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found."
        )
    return client


@router.get(
    "/active_clients/",
    response_model=List[ResponseClientModel],
    name="Get all active clients",
    # dependencies=[
    #     Depends(allowed_create_users),
    #     Depends(RateLimiter(times=2, seconds=5)),
    # ],
)
async def get_all_active_clients(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    clients = await repository_clients.get_all_active_clients_repo(db, limit, offset)
    return clients


@router.get(
    "/unactive_clients/",
    response_model=List[ResponseClientModel],
    name="Get all unactive clients",
    # dependencies=[
    #     Depends(allowed_create_users),
    #     Depends(RateLimiter(times=2, seconds=5)),
    # ],
)
async def get_all_unactive_clients(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    clients = await repository_clients.get_all_unactive_clients_repo(db, limit, offset)
    return clients


@router.get(
    "/vip_clients/",
    response_model=List[ResponseClientModel],
    name="Get all active VIP clients",
    # dependencies=[
    #     Depends(allowed_create_users),
    #     Depends(RateLimiter(times=2, seconds=5)),
    # ],
)
async def get_all_vip_clients(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    clients = await repository_clients.get_all_vip_clients_repo(db, limit, offset)
    return clients


@router.get(
    "/non_vip_clients/",
    response_model=List[ResponseClientModel],
    name="Get all active NON VIP clients",
    # dependencies=[
    #     Depends(allowed_create_users),
    #     Depends(RateLimiter(times=2, seconds=5)),
    # ],
)
async def get_all_non_vip_clients(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    clients = await repository_clients.get_all_non_vip_clients_repo(db, limit, offset)
    return clients


@router.patch(
    "/update_vip_status/",
    response_model=VIPStatusResponse,
    name="Update VIP status"
    # dependencies=[
    # Depends(allowed_create_users),
    # Depends(RateLimiter(times=2, seconds=5)),
    # ],
)
async def update_vip_status(
    body: UpdateVIPClientModel,
    new_status=Query(enum=["true", "false"]),
    db: Session = Depends(get_db),
):
    try:
        body.tax_number = int(body.tax_number)
    except AttributeError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Please enter number, not letters.",
        )
    client = await repository_clients.check_existing_client_by_tax_number(
        body.tax_number, db
    )
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found."
        )
    client = await repository_clients.update_vip_status_repo(body, new_status, db)
    return client


@router.delete(
    "/delete_client/",
    name="Delete client"
    # dependencies=[
    # Depends(allowed_create_users),
    # Depends(RateLimiter(times=2, seconds=5)),
    # ],
)
async def delete_client(
    body: UpdateVIPClientModel,
    db: Session = Depends(get_db),
):
    client = await repository_clients.check_existing_client_by_tax_number(
        body.tax_number, db
    )
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found."
        )
    remove_client = await repository_clients.delete_client_repo(body, db)
    return remove_client
