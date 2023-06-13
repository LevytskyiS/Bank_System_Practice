from sqlalchemy import Column, Integer, String, Boolean, func, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# bank_m2m_clients = Table(
#     "banks_m2m_clients",
#     Base.metadata,
#     Column("id", Integer, primary_key=True),
#     Column("client_id", Integer, ForeignKey("clients.id", ondelete="CASCADE")),
#     Column("bank_id", Integer, ForeignKey("banks.id", ondelete="CASCADE")),
# )


# class Bank(Base):
#     __tablename__ = "banks"
#     id = Column(Integer, primary_key=True)
#     bank_code = Column(Integer, nullable=False)
#     title = Column(String(100), nullable=False)
#     clients = relationship("Client", secondary=bank_m2m_clients, backref="banks")


# class Client(Base):
#     __tablename__ = "clients"
#     id = Column(Integer, primary_key=True)
#     first_name = Column(String(20), nullable=False)
#     last_name = Column(String(30), nullable=False)
#     email = Column(String(50), nullable=False, unique=True)
#     phone = Column(String, unique=True)
#     secret_word = Column(String, nullable=False)
#     passport_number = Column(String, nullable=False, unique=True)


class ClientM2MBank(Base):
    __tablename__ = "clientm2mbank"
    id = Column(Integer, primary_key=True)
    client_id = Column("client_id", ForeignKey("clients.id", ondelete="CASCADE"))
    bank_id = Column("bank_id", ForeignKey("banks.id", ondelete="CASCADE"))
    client = relationship("Client", backref="client", innerjoin=True)
    bank = relationship("Bank", backref="banks", innerjoin=True)


class Bank(Base):
    __tablename__ = "banks"
    id = Column(Integer, primary_key=True)
    bank_code = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(50), nullable=False, unique=False)
    phone = Column(String, unique=False)
    secret_word = Column(String, nullable=False)
    passport_number = Column(String, nullable=False, unique=False)


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    account_number = Column(Integer, nullable=False)
    current_deposit = Column(Integer, default=0)
    client_id = Column("client_id", ForeignKey("clients.id", ondelete="CASCADE"))
    client = relationship("Client", backref="clients", innerjoin=True)


class CreditCard(Base):
    __tablename__ = "creditcards"
    id = Column(Integer, primary_key=True)
    card_number = Column(Integer, nullable=False)
    pin_code = Column(Integer, default=0)
    account_id = Column("account_id", ForeignKey("accounts.id", ondelete="CASCADE"))
    account = relationship("Account", backref="accounts", innerjoin=True)
