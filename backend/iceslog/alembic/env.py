from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy import event

from alembic import context

import sys;
import os
parent_dir = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(parent_dir)
print(sys.path)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from iceslog.models import SQLModel  # noqa
target_metadata = SQLModel.metadata

@event.listens_for(target_metadata, 'column_reflect')
def receive_column_reflect(inspector, table, column_info):
    print("aaaaaaaaaaaaaaaaa")
    pass


@event.listens_for(target_metadata, 'before_create')
def receive_before_create(target, connection, **kw):
    "listen for the 'before_create' event"
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_url():
    # user = os.getenv("POSTGRES_USER", "postgres")
    # password = os.getenv("POSTGRES_PASSWORD", "")
    # server = os.getenv("POSTGRES_SERVER", "db")
    # port = os.getenv("POSTGRES_PORT", "5432")
    # db = os.getenv("POSTGRES_DB", "app")
    # return f"postgresql+psycopg://{user}:{password}@{server}:{port}/{db}"
    return os.getenv("SQLITE_DB", "sqlite:///./sql_app.db")

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
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
