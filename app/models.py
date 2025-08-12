from sqlmodel import Field, Session, SQLModel, create_engine, select, col


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None

sql_file_name = "database.db"
sqlite_url = f"sqlite:///{sql_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_heroes():
    hero_1 = Hero(name="name1", secret_name="name10")
    hero_2 = Hero(name="name2", secret_name="name20")
    hero_3 = Hero(name="name3", secret_name="name30", age=48)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)

        session.commit()

def select_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero).where(col(Hero.name) == "name2")).all()
        print(heroes)

def update_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(col(Hero.name) == "name2")
        results = session.exec(statement)
        hero = results.one()
        print("Hero: ", hero)

        hero.age = 16
        session.add(hero)
        session.commit()
        session.refresh(hero)
        print("updated hero: ", hero)

def main():
    create_db_and_tables()
    create_heroes()
    select_heroes()
    update_heroes()

if __name__ == "__main__":
    main()