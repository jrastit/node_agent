from logging.config import fileConfig
from alembic_utils.replaceable_entity import register_entities
from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_policy import PGPolicy
from types import ModuleType

import pkgutil
import importlib
import importlib.util
import sys
import os
import re
import inspect as pyinspect
from pathlib import Path

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


def env_flag(name: str, default: str = "0") -> bool:
    return os.getenv(name, default).strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


PGFUNCTION_TABLE_FILTER_ENABLED = env_flag(
    "ALEMBIC_FILTER_PGFUNCTION_BY_TABLES",
    "0",
)
PUBLIC_TABLE_REF_PATTERN = re.compile(
    r'\bpublic\."([^"]+)"|\bpublic\.([a-zA-Z_][a-zA-Z0-9_]*)'
)
PUBLIC_FUNCTION_REF_PATTERN = re.compile(
    r"\bpublic\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\("
)


def import_all_models():
    package_name = model_pkg.__name__
    imported_modules: set[str] = set()

    for _, module_name, _ in pkgutil.walk_packages(
        model_pkg.__path__,
        prefix=f"{package_name}.",
    ):
        importlib.import_module(module_name)
        imported_modules.add(module_name)

    package_paths = [Path(path) for path in model_pkg.__path__]
    for package_path in package_paths:
        for py_file in package_path.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue

            rel_module = py_file.relative_to(package_path).with_suffix("")
            module_name = f"{package_name}.{'.'.join(rel_module.parts)}"
            if module_name in imported_modules:
                continue

            spec = importlib.util.spec_from_file_location(module_name, py_file)
            if spec is None or spec.loader is None:
                continue

            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            imported_modules.add(module_name)


def get_alembic_entities_from_model() -> list[PGFunction | PGPolicy]:
    entities: list[PGFunction | PGPolicy] = []
    seen_ids: set[int] = set()

    for module in list(sys.modules.values()):
        if not isinstance(module, ModuleType):
            continue

        module_name = getattr(module, "__name__", "")
        if not module_name.startswith(f"{model_pkg.__name__}."):
            continue

        for _, obj in pyinspect.getmembers(module):
            if (
                isinstance(obj, (PGFunction, PGPolicy))
                and id(obj) not in seen_ids
            ):
                seen_ids.add(id(obj))
                entities.append(obj)

    return entities


def get_function_public_table_refs(function: PGFunction) -> set[str]:
    definition = getattr(function, "definition", "") or ""
    refs: set[str] = set()

    for quoted_name, plain_name in PUBLIC_TABLE_REF_PATTERN.findall(definition):
        table_name = quoted_name or plain_name
        if table_name:
            refs.add(table_name)

    return refs


def get_function_name(function: PGFunction) -> str:
    signature = getattr(function, "signature", "") or ""
    return signature.split("(", maxsplit=1)[0].strip()


def get_policy_public_function_refs(policy: PGPolicy) -> set[str]:
    definition = getattr(policy, "definition", "") or ""
    return set(PUBLIC_FUNCTION_REF_PATTERN.findall(definition))


def get_existing_public_functions(connection) -> set[str]:
    rows = connection.exec_driver_sql(
        """
        SELECT p.proname
        FROM pg_proc p
        JOIN pg_namespace n ON n.oid = p.pronamespace
        WHERE n.nspname = 'public'
        """
    )
    return {row[0] for row in rows}


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
ALEMBIC_VERSION_SCHEMA = "alembic"


def ensure_alembic_version_schema(connection) -> None:
    connection.exec_driver_sql(
        f'CREATE SCHEMA IF NOT EXISTS "{ALEMBIC_VERSION_SCHEMA}"'
    )


def enable_rls_for_all_public_tables(connection) -> None:
    public_tables = set(inspect(connection).get_table_names(schema="public"))

    for table_name in sorted(public_tables):
        if table_name == "alembic_version":
            continue
        connection.exec_driver_sql(
            f'ALTER TABLE public."{table_name}" ENABLE ROW LEVEL SECURITY'
        )


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
        version_table_schema=ALEMBIC_VERSION_SCHEMA,
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
            version_table_schema=ALEMBIC_VERSION_SCHEMA,
        )
        public_tables = set(
            inspect(connection).get_table_names(schema="public")
        )
        existing_public_functions = get_existing_public_functions(connection)
        discovered_entities = get_alembic_entities_from_model()
        function_entities: list[PGFunction] = []
        policy_entities: list[PGPolicy] = []

        for entity in discovered_entities:
            if isinstance(entity, PGPolicy):
                table_ref = entity.on_entity.split(".")[-1].strip('"')
                if table_ref in public_tables:
                    policy_entities.append(entity)
                continue

            if PGFUNCTION_TABLE_FILTER_ENABLED:
                referenced_tables = get_function_public_table_refs(entity)
                if not referenced_tables.issubset(public_tables):
                    continue

            function_entities.append(entity)

        managed_function_names = {
            get_function_name(function) for function in function_entities
        }

        entities: list[PGFunction | PGPolicy] = list(function_entities)
        for policy in policy_entities:
            referenced_functions = get_policy_public_function_refs(policy)
            missing_functions = referenced_functions - (
                managed_function_names | existing_public_functions
            )
            if missing_functions:
                continue
            entities.append(policy)

        register_entities(
            entities,
            "public",
            entity_types=[PGFunction, PGPolicy],
        )

        with context.begin_transaction():
            ensure_alembic_version_schema(connection)
            context.run_migrations()
            enable_rls_for_all_public_tables(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
