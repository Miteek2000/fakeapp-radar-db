import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool
from sqlalchemy.engine import URL

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name, disable_existing_loggers=False)


def database_url() -> URL:
    """Arma la conexión con las variables POSTGRES_* (así la contraseña puede traer cualquier símbolo)."""
    try:
        return URL.create(
            "postgresql+psycopg",
            username=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            host=os.environ.get("POSTGRES_HOST", "localhost"),
            port=int(os.environ.get("POSTGRES_PORT", "5432")),
            database=os.environ["POSTGRES_DB"],
        )
    except KeyError as missing:
        raise RuntimeError(f"Falta la variable de entorno {missing}") from None


# Las migraciones se escriben a mano (no se generan desde el código de la API).
target_metadata = None


def run_migrations_online() -> None:
    # Se pasa el objeto URL (no texto): así la contraseña puede traer cualquier símbolo.
    connectable = create_engine(database_url(), poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
