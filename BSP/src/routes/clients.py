from fastapi import APIRouter, status, Depends, Form, Query
from fastapi_limiter.depends import RateLimiter

from sqlalchemy.orm import Session

from src.database.models import Client
from src.schemas.clients import ClientModel
from src.database.connect import get_db
from src.repository import clients as repository_clients

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post(
    "/",
    # response_model=ClientModel,
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
    body.sex = sex
    user = await repository_clients.create_client(body, db)
    # check_mail = await repository_users.check_exist_mail(body, db)
    # if check_mail:
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail="Such mail already registered",
    #     )
    # check_username = await repository_users.check_exist_username(body, db)
    # if check_username:
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail="Such username already registered",
    #     )
    # body.password = auth_service.get_password_hash(body.password)
    # user = await repository_users.create_user(body, db)
    return {"detail": "Client was created"}
