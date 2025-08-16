from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select

from .models import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/banks/")
async def create_banks(bank: Bank):
    with Session(engine) as session:
        session.add(bank)
        session.commit()
        session.refresh(bank)
        return bank

@app.get("/banks/")
async def read_all_banks():
    with Session(engine) as session:
        banks = session.exec(select(Bank)).all()
        return banks

@app.patch("/banks/{bank_id}", response_model=BankPublic)
async def update_banks(bank_id: int, bank: BankUpdate):
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
async def create_heroes(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero

@app.get("/heroes/")
async def select_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes

@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
async def update_heroes(hero_id: int, hero: HeroUpdate):
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

@app.delete("/heroes/{hero_id}")
async def delete_heroes(hero_id: int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        session.delete(hero)
        session.commit()
        return {"ok": True}

@app.get("/cards/")
async def select_cards():
    with Session(engine) as session:
        cards = session.exec(select(Card)).all()
        return cards

@app.post("/cards/")
async def create_cards(card: Card):
    with Session(engine) as session:
        session.add(card)
        session.commit()
        session.refresh(card)
        return card

@app.patch("/cards/{card_id}", response_model=Card)
async def update_cards(card_id: int, card: Card):
    with Session(engine) as session:
        db_card = session.get(Card, card_id)
        if not db_card:
            raise HTTPException(status_code=404, detail="Card not found")
        card_data = card.model_dump(exclude_unset=True)
        db_card.sqlmodel_update(card_data)
        session.add(db_card)
        session.commit()
        session.refresh(db_card)
        return db_card

@app.delete("/cards/{card_id}")
async def delete_cards(card_id: int):
    with Session(engine) as session:
        card = session.get(Card, card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")
        session.delete(card)
        session.commit()
        return {"ok": True}