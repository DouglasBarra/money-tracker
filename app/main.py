from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select, col

from models import *

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/banks/")
def create_banks(bank: Bank):
    with Session(engine) as session:
        session.add(bank)
        session.commit()
        session.refresh(bank)
        return bank

@app.get("/banks/")
def read_all_banks():
    with Session(engine) as session:
        banks = session.exec(select(Bank)).all()
        return banks

@app.patch("/banks/{bank_id}", response_model=BankPublic)
def update_banks(bank_id: int, bank: BankUpdate):
    with Session(engine) as session:
        db_bank = session.get(Bank, bank_id)
        if not db_bank:
            raise HTTPException(status_code=404, detail="Bank not found")
        bank_data = bank.model_dump(exclude_unset=True)
        db_bank.sqlmodel_update(bank_data)
        session.add(db_bank)
        session.commit()
        session.refresh(db_bank)
        return db_bank

@app.post("/heroes/")
def create_heroes(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero

@app.get("/heroes/")
def select_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes

@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_heroes(hero_id: int, hero: HeroUpdate):
    with Session(engine) as session:
        db_hero = session.get(Hero, hero_id)
        if not db_hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        hero_data = hero.model_dump(exclude_unset=True)
        db_hero.sqlmodel_update(hero_data)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero


def delete_heroes(hero_id: int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        session.delete(hero)
        session.commit()
        return {"ok": True}


def main():
    create_db_and_tables()

if __name__ == "__main__":
    main()