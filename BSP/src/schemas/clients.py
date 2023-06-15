from pydantic import BaseModel, Field, EmailStr


class ClientModel(BaseModel):
    first_name: str = Field()
    last_name: str = Field()
    email: EmailStr = Field()
    phone: int = Field()
    secret_word: str = Field()
    passport_number: str = Field()
    sex: str = Field(default="")

    # first_name = Column(String(20), nullable=False)
    # last_name = Column(String(30), nullable=False)
    # email = Column(String(50), nullable=False, unique=True)
    # phone = Column(String, unique=True)
    # secret_word = Column(String, nullable=False)
    # passport_number = Column(String, nullable=False, unique=True)
    # sex = Column(String(6), nullable=False)
