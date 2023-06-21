from pydantic import BaseModel, Field


class AccountNumber(BaseModel):
    account_id: int = Field(ge=0)


class CreditCardResponseModel(BaseModel):
    card_number: int
    account_id: int
    activated: bool

    class Config:
        orm_mode = True
