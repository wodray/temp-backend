import sys

sys.path.append("C:\\dev\\py\\temp-backend\\src")

from rich import print
from sqlmodel import Field, Relationship, Session, SQLModel, select

from database import engine


class HeroTeamLink(SQLModel, table=True):
    team_id: int | None = Field(default=None, foreign_key="team.id", primary_key=True)
    hero_id: int | None = Field(default=None, foreign_key="hero.id", primary_key=True)
    is_training: bool = False  # 额外字段

    team: "Team" = Relationship(back_populates="hero_links")  # 明确的多对一关系
    hero: "Hero" = Relationship(back_populates="team_links")  # 明确的多对一关系


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    # heroes: list["Hero"] = Relationship(back_populates="teams", link_model=HeroTeamLink)
    hero_links: list[HeroTeamLink] = Relationship(back_populates="team")


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    # teams: list[Team] = Relationship(back_populates="heroes", link_model=HeroTeamLink)
    team_links: list[HeroTeamLink] = Relationship(back_populates="hero")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    # with Session(engine) as session:
    #     team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
    #     team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

    #     hero_deadpond = Hero(
    #         name="Deadpond",
    #         secret_name="Dive Wilson",
    #         teams=[team_z_force, team_preventers],
    #     )
    #     hero_rusty_man = Hero(
    #         name="Rusty-Man",
    #         secret_name="Tommy Sharp",
    #         age=48,
    #         teams=[team_preventers],
    #     )
    #     hero_spider_boy = Hero(
    #         name="Spider-Boy", secret_name="Pedro Parqueador", teams=[team_preventers]
    #     )
    #     session.add(hero_deadpond)
    #     session.add(hero_rusty_man)
    #     session.add(hero_spider_boy)
    #     session.commit()

    #     session.refresh(hero_deadpond)
    #     session.refresh(hero_rusty_man)
    #     session.refresh(hero_spider_boy)

    #     print("Deadpond:", hero_deadpond)
    #     print("Deadpond teams:", hero_deadpond.teams)
    #     print("Rusty-Man:", hero_rusty_man)
    #     print("Rusty-Man Teams:", hero_rusty_man.teams)
    #     print("Spider-Boy:", hero_spider_boy)
    #     print("Spider-Boy Teams:", hero_spider_boy.teams)

    # 含有额外字段
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

        hero_deadpond = Hero(
            name="Deadpond",
            secret_name="Dive Wilson",
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
        )
        hero_spider_boy = Hero(
            name="Spider-Boy",
            secret_name="Pedro Parqueador",
        )
        deadpond_team_z_link = HeroTeamLink(team=team_z_force, hero=hero_deadpond)
        deadpond_preventers_link = HeroTeamLink(
            team=team_preventers, hero=hero_deadpond, is_training=True
        )
        spider_boy_preventers_link = HeroTeamLink(
            team=team_preventers, hero=hero_spider_boy, is_training=True
        )
        rusty_man_preventers_link = HeroTeamLink(
            team=team_preventers, hero=hero_rusty_man
        )

        session.add(deadpond_team_z_link)
        session.add(deadpond_preventers_link)
        session.add(spider_boy_preventers_link)
        session.add(rusty_man_preventers_link)
        session.commit()

        for link in team_z_force.hero_links:
            print("Z-Force hero:", link.hero, "is training:", link.is_training)

        for link in team_preventers.hero_links:
            print("Preventers hero:", link.hero, "is training:", link.is_training)


def update_heroes():
    # with Session(engine) as session:
    #     hero_spider_boy = session.exec(
    #         select(Hero).where(Hero.name == "Spider-Boy")
    #     ).one()
    #     team_z_force = session.exec(select(Team).where(Team.name == "Z-Force")).one()

    #     team_z_force.heroes.append(hero_spider_boy)
    #     session.add(team_z_force)
    #     session.commit()

    #     print("Updated Spider-Boy's Teams:", hero_spider_boy.teams)
    #     print("Z-Force heroes:", team_z_force.heroes)

    #     hero_spider_boy.teams.remove(team_z_force)
    #     session.add(team_z_force)
    #     session.commit()

    #     print("Reverted Z-Force's heroes:", team_z_force.heroes)
    #     print("Reverted Spider-Boy's teams:", hero_spider_boy.teams)

    # 包含额外字段
    with Session(engine) as session:
        hero_spider_boy = session.exec(
            select(Hero).where(Hero.name == "Spider-Boy")
        ).one()
        team_z_force = session.exec(select(Team).where(Team.name == "Z-Force")).one()

        spider_boy_z_force_link = HeroTeamLink(
            team=team_z_force, hero=hero_spider_boy, is_training=True
        )
        team_z_force.hero_links.append(spider_boy_z_force_link)
        session.add(team_z_force)
        session.commit()

        print("Updated Spider-Boy's Teams:", hero_spider_boy.team_links)
        print("Z-Force heroes:", team_z_force.hero_links)

        for link in hero_spider_boy.team_links:
            if link.team.name == "Preventers":
                link.is_training = False

        session.add(hero_spider_boy)
        session.commit()

        for link in hero_spider_boy.team_links:
            print("Spider-Boy team:", link.team, "is training:", link.is_training)


def main():
    create_db_and_tables()
    # create_heroes()
    update_heroes()


if __name__ == "__main__":
    main()
