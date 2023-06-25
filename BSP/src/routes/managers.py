from fastapi import APIRouter, status, Depends, Query, HTTPException
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.models import Roles
from src.database.connect import get_db
from src.schemas.managers import ManagerModel, ResponseManagerModel, ChangeRoleModel
from src.repository import managers as repository_managers
from src.services.roles import RolesChecker
from src.services.auth import auth_service

router = APIRouter(prefix="/managers", tags=["managers"])

allowed_create_managers = RolesChecker([Roles.admin, Roles.team_leader])
allowed_update_managers = RolesChecker([Roles.admin, Roles.team_leader, Roles.manager])


@router.post(
    "/",
    response_model=ResponseManagerModel,
    name="Create manager",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(allowed_create_managers),
        # Depends(RateLimiter(times=2, seconds=5)),
    ],
)
async def create_manager(body: ManagerModel, db: Session = Depends(get_db)):
    check_manager = await repository_managers.check_existing_manager_by_email(
        body.email, db
    )
    if check_manager:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Manager with such e-mail is already registered.",
        )
    body.password = auth_service.get_password_hash(body.password)
    manager = await repository_managers.create_manager_repo(body, db)
    return manager


@router.patch(
    "/change_role/",
    response_model=ResponseManagerModel,
    name="Change manager's role",
    dependencies=[
        Depends(allowed_update_managers),
        # Depends(RateLimiter(times=2, seconds=5)),
    ],
)
async def change_role(
    body: ChangeRoleModel,
    role=Query(enum=["admin", "director", "team_leader", "manager"]),
    db: Session = Depends(get_db),
):
    check_manager = await repository_managers.check_existing_manager_by_email(
        body.email, db
    )
    if not check_manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manager not found.",
        )
    manager = await repository_managers.change_role_repo(body, role, db)
    return manager


@router.delete(
    "/delete_manager/",
    name="Delete manager",
    dependencies=[
        Depends(allowed_create_managers),
        # Depends(RateLimiter(times=2, seconds=5)),
    ],
)
async def delete_manager(
    body: ChangeRoleModel,
    db: Session = Depends(get_db),
):
    check_manager = await repository_managers.check_existing_manager_by_email(
        body.email, db
    )
    if not check_manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manager not found.",
        )
    remove_manager = await repository_managers.remove_manager_repo(body, db)
    return remove_manager
