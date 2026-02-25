from logging.config import fileConfig
from alembic_utils.replaceable_entity import register_entities
from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_policy import PGPolicy
from node_agent.model.function.psql_user_management import (
    current_user_id,
    is_org_member,
    is_user,
)
from node_agent.model.server import server_select_policy
from node_agent.model.function.psql_discover import list_public_tables

import pkgutil
import importlib

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy import inspect


from alembic import context

from node_agent.config import get_database_uri
import node_agent.model as model_pkg  # <- IMPORTANT


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2) Importer metadata SQLAlchemy

from node_agent.myapp import init_app

app = init_app()

from node_agent.model.db import Base


def import_all_models():
    package = model_pkg
    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        if is_pkg:
            continue
        importlib.import_module(f"{package.__name__}.{module_name}")


import_all_models()

print("METADATA TABLES:", sorted(Base.metadata.tables.keys()))

target_metadata = Base.metadata

# def build_db_url() -> str:
#     user = settings.get("DB_USER") or settings.get("db_user")
#     password = settings.get("DB_PASSWORD") or settings.get("db_password")
#     host = settings.get("DB_HOST") or settings.get("db_host")
#     port = settings.get("DB_PORT") or settings.get("db_port", 5432)
#     name = settings.get("DB_NAME") or settings.get("db_name", "postgres")
#     sslmode = settings.get("DB_SSLMODE") or settings.get("db_sslmode", "require")

#     # driver: psycopg2 ou psycopg (selon ton install)
#     driver = settings.get("DB_DRIVER") or "postgresql+psycopg2"

#     # URL SQLAlchemy
#     return f"{driver}://{user}:{password}@{host}:{port}/{name}?sslmode={sslmode}"

# 3) Écraser l’URL d’alembic.ini dynamiquement
config.set_main_option("sqlalchemy.url", get_database_uri())


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        public_tables = set(
            inspect(connection).get_table_names(schema="public")
        )
        entities = [list_public_tables]

        if "user" in public_tables:
            entities.extend([is_user, current_user_id])

        if {"user", "group", "user_group_association"}.issubset(public_tables):
            entities.append(is_org_member)

        if {
            "server",
            "organisation",
            "user",
            "group",
            "user_group_association",
        }.issubset(public_tables):
            entities.append(server_select_policy)

        register_entities(
            entities,
            "public",
            entity_types=[PGFunction, PGPolicy],
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
