from pydantic import BaseModel, Field


class AccountNumber(BaseModel):
    account_id: int = Field(ge=0)


class CreditCardResponseModel(BaseModel):
    card_number: int
    account_id: int
    activated: bool

    class Config:
        orm_mode = True


class DeactivateCard(BaseModel):
    client_tax_number: int = Field(gt=0)
    card_number: int = Field(gt=0)


class CreditCardSearchModel:
    card_number: int = Field(gt=0)
