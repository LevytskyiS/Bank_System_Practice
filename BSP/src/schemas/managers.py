from pydantic import BaseModel, Field, EmailStr
from src.database.models import Roles


class ManagerModel(BaseModel):
    first_name: str = Field(min_length=1, max_length=20)
    last_name: str = Field(min_length=1, max_length=30)
    email: EmailStr
    phone: int = Field(gt=100000000, le=999999999)
    password: str = Field(min_length=6, max_length=20)


class ResponseManagerModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: int
    roles: Roles
    active: bool

    class Config:
        orm_mode = True


class ChangeRoleModel(BaseModel):
    email: EmailStr
