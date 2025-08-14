from sqlmodel import Field

from app.database import *

class Bank(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

class BankBase(SQLModel):
    name: str
    code: int

class BankCreate(BankBase):
    pass

class BankPublic(SQLModel):
    id: int

class BankUpdate(SQLModel):
    name: str | None = None
    code: int | None = None

class Card(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    bank_id: int | None = Field(default=None, foreign_key="bank.id")
    debit: bool
    credit: bool
    description: str | None = None

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

class HeroBase(SQLModel):
    name: str
    secret_name: str
    age: int | None = None

class HeroCreate(HeroBase):
    pass

class HeroPublic(HeroBase):
    id: int

class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None

