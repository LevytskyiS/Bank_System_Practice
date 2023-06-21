from sqlalchemy import Column, Integer, String, Boolean, func, Table, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


# class ClientM2MBank(Base):
#     __tablename__ = "clientm2mbank"
#     id = Column(Integer, primary_key=True)
#     client_id = Column("client_id", ForeignKey("clients.id", ondelete="CASCADE"))
#     bank_id = Column("bank_id", ForeignKey("banks.id", ondelete="CASCADE"))
#     client = relationship("Client", backref="client", innerjoin=True)
#     bank = relationship("Bank", backref="banks", innerjoin=True)


# class Bank(Base):
#     __tablename__ = "banks"
#     id = Column(Integer, primary_key=True)
#     bank_code = Column(Integer, nullable=False)
#     title = Column(String(100), nullable=False)


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(30), nullable=False)
    tax_number = Column(BigInteger, nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(String, unique=True)
    secret_word = Column(String, nullable=False)
    passport_number = Column(String, nullable=False, unique=True)
    sex = Column(String(6), nullable=False)
    vip = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    trusted = Column(Boolean, default=True)


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    account_number = Column(String(50), nullable=False)
    current_deposit = Column(Integer, default=0)
    active = Column(Boolean, default=True)
    client_id = Column("client_id", ForeignKey("clients.id", ondelete="CASCADE"))
    client = relationship("Client", backref="clients", innerjoin=True)


class CreditCard(Base):
    __tablename__ = "creditcards"
    id = Column(Integer, primary_key=True)
    card_number = Column(BigInteger, nullable=False)
    pin_code = Column(Integer, default=0)
    account_id = Column("account_id", ForeignKey("accounts.id", ondelete="CASCADE"))
    account = relationship("Account", backref="accounts", innerjoin=True)
    activated = Column(Boolean, default=False)
