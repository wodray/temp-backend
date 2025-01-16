# backend

脚本在哪里，导入查找的路径（`sys.path`）就从哪里开始

## Alembic

创建迁移环境

```shell
alembic init alembic
```

配置自动生成迁移，编辑`env.py`

```python
# from myapp.mymodel import Base # SQLAlchemy
from myapp.mymodel import SQLModel # SQLModel

# target_metadata = Base.metadata
target_metadata = SQLModel.metadata # SQLModel

# 从应用配置中获取数据库连接
from myapp.mymodel import DATABASE_URL
config.set_main_option('sqlalchemy.url', DATABASE_URL)
```

> 自动生成无法检测：
>
> - 表名更改
> - 列名更改
> - 匿名命名的约束
> - 特殊 SQLAlchemy 类型，如 Enum ，在不支持 ENUM 的后端生成时 - 这是因为在非支持数据库中此类类型的表示，即 CHAR+ CHECK 约束，可以是任何类型的 CHAR+CHECK。

检查数据库模型是否产生了变化

```shell
alembic check
```

创建迁移脚本

```shell
alembic revision -m "create account table"

# 主要还是使用自动生成迁移
alembic revision --autogenerate -m "Added account table"
```

运行迁移

```shell
# 至最新版本
alembic upgrade head

# 指定要升级到的版本
alembic upgrade 1975ea83b712
```

离线模式：Alembic 的一项主要功能是将迁移作为 SQL 脚本生成，而不是在数据库中运行，这也被称为离线模式。在访问 DDL 受限、SQL 脚本必须交给 DBA 的大型企业中，这是一项至关重要的功能。
> 请注意，我们的迁移脚本从base开始--这是使用脱机模式时的默认情况，因为没有数据库连接，也没有 alembic_version 表可供读取。

```shell
# 输出 SQL
alembic upgrade ae1027a6acf --sql

# 重定向生成 SQL 脚本
alembic upgrade ae1027a6acf --sql > migration.sql
```

相对迁移

```shell
# 从当前版本升级两个版本
alembic upgrade +2

# 从当前版本降级1个版本
alembic downgrade -1

# 升级到版本 ae1027a6acf 加上两个额外步骤
alembic upgrade ae10+2
```

获取信息

```shell
# 查看当前的修订版本
alembic current

# 查看历史记录
alembic history --verbose

# 查看特定范围历史：使用 -r 选项，-r参数接受一个参数 [start]:[end]

# 从三次修订前，到当前迁移的相对范围
alembic history -r-3:current

# 查看从 1975 年到标题的所有修订：
alembic history -r1975ea:
```

降级

```shell
# 回到起点，降级为无
alembic downgrade base
```

## SQLAlchemy/SQLModel

由于 SQLModel 类模型既是 SQLAlchemy 模型，也是 Pydantic 模型。所以可以使用相同的模型来定义 API 将接收的 request body。模型（Pydantic 部分）将进行自动数据验证，并把 JSON 请求转换为 Hero 类实际实例的对象。然后，由于这个相同的 SQLModel 对象不仅是 Pydantic 模型实例，也是 SQLAlchemy 模型实例，因此我们可以在 session 中直接使用它在数据库中创建行。（不适用于所有情况）

```python
@app.post("/heroes/", response_model=Hero)
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero
```

这样，我们可以使用直观的标准 Python 类型注解，而不必为数据库模型和 API 数据模型重复编写大量代码。

何时使用模型继承法则：

- 仅从 data model 继承
  
  只从 data model 继承，不从 table model 继承。这将帮助您避免混淆，而且您也没有任何理由需要从 table model 继承。

  如果您觉得需要从 table model 继承，那么请创建一个 基类，该类仅是一个 data model，并拥有所有这些字段，如 HeroBase 类。

  然后从该 base 类继承，该类对于任何其他 data model 和 table model 来说，都只是一个 data model。

- 避免重复 - 保持简单
  
  如果为了避免一些重复，你最终会得到一棵疯狂的具有继承性的模型树，那么更简单的做法可能是复制其中的一些字段，这样可能更容易推理和维护。

  总之，做任何更容易推理、编程、维护和重构的事情。

> 定义模型时，`table=True` 的是表模型，没有的是数据模型

字段/列的默认值配置：

- default: 在 Python 端处理，适用于需要在应用程序逻辑中控制默认值的场景。
- server_default: 在数据库端处理，适用于需要依赖数据库的默认值（如数据库触发器、序列等）的场景。

模型类属性、和实例：每个列/字段的模型类属性都很特殊，可用于表达式。但这只适用于模型类属性。实例属性的行为与普通Python 值相同。

### 关系

- 关系配置
  - 只要在 当前模型中，该行就与当前模型有关。
  - 属性名称是关于 other 模型的。
  - 类型注释是关于 other 模型的。
  - 而 back_populates 指的是 other 模型中的一个属性，该属性指向当前模型。

- `Relationship()` 中的 `back_populates` 参数是什么？
  
  这会告诉 SQLModel，如果此模型中的内容发生变化，它就会在另一个模型中更改该属性，甚至在提交会话（这将强制刷新数据）之前也会这样做。

- 关系在 Python 侧删除被外键引用的记录的默认行为是：SQLModel（实际上是 SQLAlchemy）将访问包含外键的记录，并将外键列设为 NULL。

- 如果您知道您的数据库能够自行正确处理删除或更新，只需使用 `ondelete="CASCADE"` 或 `ondelete="SET NULL"` 即可、您可以在 `Relationship()` 中使用 `passive_deletes="all"` 来告诉 SQLModel（实际上是 SQLAlchemy），在为被外键引用的表发送 DELETE 之前， 不要删除或更新这些记录（对于含外键表）。

- 在某些情况下，如果您想自动级联删除一条记录到其相关记录（删除一个团队及其英雄），您可以这样做：
  - 在无外键一侧的`Relationship()`中使用`cascade_delete=True`。
  - 并在 `Field()` 中使用 `ondelete="CASCADE"` 和 Foreign key 。

- 配置在有相关记录（Hero）的情况下防止删除记录（Team）：
  - 在模型表 Hero 中的 `Field()` 外键 team_id 中设置 `ondelete="RESTRICT"` 。
  - 在 Team 模型表中，在 Hero 的 `Relationship()` 中使用 `passive_deletes="all"`，这样，将删除模型的外键设置为 NULL 的默认行为将被禁用，当我们尝试删除一个包含 Hero 的 Team 时，数据库将引发错误。

#### 多对多关系

通过增加一个中间层即关联模型实现：

```python
# 不需要直接与 HeroTeamLink 模型交互，而是通过自动的多对多关系进行交互。
class HeroTeamLink(SQLModel, table=True):
    team_id: int | None = Field(default=None, foreign_key="team.id", primary_key=True)
    hero_id: int | None = Field(default=None, foreign_key="hero.id", primary_key=True)

class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: list["Hero"] = Relationship(back_populates="teams", link_model=HeroTeamLink)

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    teams: list[Team] = Relationship(back_populates="heroes", link_model=HeroTeamLink)
```

带有额外字段的链接模型

如果我们需要额外的数据来描述两个模型之间的联系呢？比方说，我们希望有一个额外的字段/列来说明某个英雄是否仍在该团队中接受训练，或者他们是否已经开始执行任务等。

处理方法是显式使用链接模型，以便能够获取和修改其数据（除了指向 Hero 和 Team 两个模型的外键）。最终，它的工作方式就像两个 一对多关系的组合。

```python
class HeroTeamLink(SQLModel, table=True):
    team_id: int | None = Field(default=None, foreign_key="team.id", primary_key=True)
    hero_id: int | None = Field(default=None, foreign_key="hero.id", primary_key=True)
    is_training: bool = False

    team: "Team" = Relationship(back_populates="hero_links")
    hero: "Hero" = Relationship(back_populates="team_links")


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    hero_links: list[HeroTeamLink] = Relationship(back_populates="team")


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_links: list[HeroTeamLink] = Relationship(back_populates="hero")

# 此时要手动创建 显式链接模型，指向其英雄和团队实例，并指定附加链接数据
deadpond_team_z_link = HeroTeamLink(team=team_z_force, hero=hero_deadpond)
deadpond_preventers_link = HeroTeamLink(team=team_preventers, hero=hero_deadpond,is_training=True)
```

在 `model.model_validate()` 中使用 update 参数，以便在创建新对象时提供额外数据，以及在更新现有对象时使用 `model.sqlmodel_update()` 参数，以便提供额外数据。

## 参考

- [源码](https://gitee.com/Barry_Python_web/python_web_code)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [FastAPI 最佳实践](https://github.com/zhanymkanov/fastapi-best-practices)
- [一个使用 FastAPI、Pydantic 2.0、Alembic 和异步 SQLModel 作为 ORM 的项目模板](https://github.com/jonra1993/fastapi-alembic-sqlmodel-async)
- [FastAPI with Async SQLAlchemy, SQLModel, and Alembic](https://testdriven.io/blog/fastapi-sqlmodel/)
- [How to Use Alembic for Database Migrations in Your FastAPI Application](https://www.nashruddinamin.com/blog/how-to-use-alembic-for-database-migrations-in-your-fastapi-application)
- [MySQL时区的查看和设置](https://blog.csdn.net/leo3070/article/details/118146780)
- [TIMESTAMP 和 DATETIME 的自动初始化和更新](https://dev.mysql.com/doc/refman/8.4/en/timestamp-initialization.html)
- [Argon2 for Python](https://argon2-cffi.readthedocs.io/en/stable/index.html)
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/index.html)
- [Redis Python client](https://github.com/redis/redis-py)
