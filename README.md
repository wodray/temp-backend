# backend

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

- 字段/列的默认值配置：
  - default: 在 Python 端处理，适用于需要在应用程序逻辑中控制默认值的场景。
  - server_default: 在数据库端处理，适用于需要依赖数据库的默认值（如数据库触发器、序列等）的场景。

- 模型类属性、和实例：

  每个列/字段的模型类属性都很特殊，可用于表达式。但这只适用于模型类属性。实例属性的行为与普通Python 值相同。

## 参考

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [FastAPI 最佳实践](https://github.com/zhanymkanov/fastapi-best-practices)
- [一个使用 FastAPI、Pydantic 2.0、Alembic 和异步 SQLModel 作为 ORM 的项目模板](https://github.com/jonra1993/fastapi-alembic-sqlmodel-async)
- [FastAPI with Async SQLAlchemy, SQLModel, and Alembic](https://testdriven.io/blog/fastapi-sqlmodel/)
- [How to Use Alembic for Database Migrations in Your FastAPI Application](https://www.nashruddinamin.com/blog/how-to-use-alembic-for-database-migrations-in-your-fastapi-application)
- [MySQL时区的查看和设置](https://blog.csdn.net/leo3070/article/details/118146780)
- [TIMESTAMP 和 DATETIME 的自动初始化和更新](https://dev.mysql.com/doc/refman/8.4/en/timestamp-initialization.html)
