from pydantic import BaseModel, Field, EmailStr


class AccountModel(BaseModel):
    tax_number: int = Field(
        gt=1000000, description="The client ID must be greated that 0."
    )


class AccountResponseModel(BaseModel):
    id: int
    account_number: str

    class Config:
        orm_mode = True
