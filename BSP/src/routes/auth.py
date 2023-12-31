import uuid

from typing import List

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
    Security,
    BackgroundTasks,
    Request,
)
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.schemas.managers import ManagerModel, ResponseManagerModel
from src.schemas.auth import (
    TokenModel,
    RequestEmail,
    ResetPasswordModel,
)
from src.repository import managers as repository_managers
from src.services.auth import auth_service

from src.services.email import send_email, send_email_reset_password_token

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post(
    "/signup", response_model=ResponseManagerModel, status_code=status.HTTP_201_CREATED
)
async def signup(
    body: ManagerModel,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    exist_manager = await repository_managers.check_existing_manager_by_email(
        body.email, db
    )
    if exist_manager:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    body.password = auth_service.get_password_hash(body.password)
    manager = await repository_managers.create_manager_repo(body, db)
    background_tasks.add_task(
        send_email, manager.email, manager.first_name, request.base_url
    )
    return manager


@router.post("/login", response_model=TokenModel)
async def login(
    body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    manager = await repository_managers.check_existing_manager_by_email(
        body.username, db
    )
    if manager is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
        )
    if not manager.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed"
        )
    if not auth_service.verify_password(body.password, manager.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    # Generate JWT
    access_token = await auth_service.create_access_token(
        data={"sub": manager.email}, expires_delta=7200
    )
    refresh_token = await auth_service.create_refresh_token(data={"sub": manager.email})
    await repository_managers.update_token_repo(manager, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# @router.get("/refresh_token", response_model=TokenModel)
# async def refresh_token(
#     credentials: HTTPAuthorizationCredentials = Security(security),
#     db: Session = Depends(get_db),
# ):
#     token = credentials.credentials
#     email = await auth_service.decode_refresh_token(token)
#     manager = await repository_managers.check_existing_manager_by_email(email, db)
#     if manager.refresh_token != token:
#         await repository_managers.update_token_repo(manager, None, db)
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
#         )

#     access_token = await auth_service.create_access_token(data={"sub": email})
#     refresh_token = await auth_service.create_refresh_token(data={"sub": email})
#     await repository_managers.update_token_repo(manager, refresh_token, db)
#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token,
#         "token_type": "bearer",
#     }


@router.get("/confirmed_email")
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    email = await auth_service.get_email_from_token(token)
    manager = await repository_managers.check_existing_manager_by_email(email, db)
    if manager is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error"
        )
    if manager.confirmed:
        return {"message": "Your e-mail is already confirmed."}
    await repository_managers.confirmed_email_repo(email, db)
    return {"message": "Email confirmed"}


@router.post("/request_email")
async def request_email(
    body: RequestEmail,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    manager = await repository_managers.check_existing_manager_by_email(body.email, db)

    if manager.confirmed:
        return {"message": "Your email is already confirmed."}
    if manager:
        background_tasks.add_task(
            send_email, manager.email, manager.first_name, request.base_url
        )
    return {"message": "Check your email for confirmation."}


@router.get(
    "/forgot_password",
    name="Forgot password",
    # dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def forgot_password(
    email: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    manager = await repository_managers.check_existing_manager_by_email(email, db)
    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found or doesn't exist."
        )
    reset_password_token = uuid.uuid1()
    background_tasks.add_task(
        send_email_reset_password_token,
        reset_password_token,
        manager.email,
        manager.first_name,
    )

    manager.reset_password_token = reset_password_token
    db.commit()

    return {
        "message": f"Reset password token has been sent to your e-email.{reset_password_token}"
    }


@router.patch(
    "/reset_password",
    name="Reset password",
    response_model=ResponseManagerModel,
    dependencies=[
        # Depends(RateLimiter(times=2, seconds=5)),
    ],
)
async def reset_password(
    body: ResetPasswordModel,
    db: Session = Depends(get_db),
):
    manager = await repository_managers.check_existing_manager_by_email(body.email, db)
    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found or doesn't exist."
        )

    if body.reset_password_token != manager.reset_password_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Password reset tokens doesn't match.",
        )

    if body.password != body.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="New password is not match."
        )

    body.password = auth_service.get_password_hash(body.password)
    manager.password = body.password
    manager.reset_password_token = None
    db.commit()

    return manager
