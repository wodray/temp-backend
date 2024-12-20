import sys

sys.path.append("C:\\dev\\py\\temp-backend\\src")

from rich import print
from sqlmodel import Field, Session, SQLModel, select

from database import engine


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
    hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
    hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
    hero_7 = Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.add(hero_4)
        session.add(hero_5)
        session.add(hero_6)
        session.add(hero_7)

        session.commit()


def select_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.age > 0).offset(1).limit(2)
        results = session.exec(statement)
        # hero = results.first()
        # hero = results.one()  # 正好一条记录，否则出错
        # hero = session.get(Hero, 1)  # 使用 主键通过 Id 列选择单行
        heroes = results.all()
        # for hero in results:
        print(heroes)


def update_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero = results.one()
        print(hero)

        hero.age = 16
        hero.name = "Spider-Youngster"
        session.add(hero)  # ? 不添加也可以生效
        session.commit()
        session.refresh(hero)
        print(hero)


def delete_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Youngster")
        results = session.exec(statement)
        hero = results.one()
        print(hero)

        session.delete(hero)
        session.commit()

        print("deleted hero", hero)

        statement = select(Hero).where(Hero.name == "Spider-Youngster")
        results = session.exec(statement)
        hero = results.first()

        if hero is None:
            print("There's no hero named Spider-Youngster")


def main():
    # create_db_and_tables()
    # create_heroes()
    # select_heroes()
    # update_heroes()
    delete_heroes()


if __name__ == "__main__":
    main()
