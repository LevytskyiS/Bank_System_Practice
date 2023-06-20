from pydantic import BaseModel, Field, EmailStr


class AccountModel(BaseModel):
    tax_number: int = Field(
        gt=1000000, description="The client ID must be greated than 0."
    )


class AccountResponseModel(BaseModel):
    id: int
    account_number: str

    class Config:
        orm_mode = True


class ToDepositCash(BaseModel):
    account_number: str
    amount: float = Field(gt=0)


class CurrentDepositResponseModel(BaseModel):
    account_number: str
    current_deposit: int

    class Config:
        orm_mode = True


class ToWithdrawCash(BaseModel):
    account_number: str
    amount: float = Field(gt=0)
