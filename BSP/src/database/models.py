from sqlalchemy import Column, Integer, String, Boolean, func, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Bank(Base):
    __tablename__ = "banks"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(30), nullable=False)


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    account_number = Column(Integer, nullable=False)


class CreditCard(Base):
    __tablename__ = "creditcards"
    id = Column(Integer, primary_key=True)
    card_number = Column(Integer, nullable=False)
