from pydantic import BaseModel, Field, EmailStr


class ClientModel(BaseModel):
    first_name: str = Field(min_length=1, max_length=20)
    last_name: str = Field(min_length=1, max_length=30)
    tax_number: int = Field(gt=1000000, le=9999999)
    email: EmailStr
    city: str = Field(min_length=3, max_length=20)
    phone: int = Field(gt=100000000, le=999999999)
    secret_word: str = Field(min_length=5)
    passport_number: str = Field()


class ClientDBModel(BaseModel):
    class Config:
        orm_mode = True


class ResponseClientModel(ClientDBModel):
    id: int
    first_name: str
    last_name: str
    tax_number: int
    email: EmailStr
    phone: int
    passport_number: str


class UpdateVIPClientModel(BaseModel):
    tax_number: int


class VIPStatusResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    vip: bool

    class Config:
        orm_mode = True
