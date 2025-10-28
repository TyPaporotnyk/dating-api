import asyncio

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from geoalchemy2 import alembic_helpers

from dating.logging import logging, configure_logging
from dating.config import SQLALCHEMY_DATABASE_URI
from dating.database.core import BaseModel
from dating.database.models import *

config = context.config

configure_logging()
logger = logging.getLogger(__name__)

config.set_main_option("sqlalchemy.url", str(SQLALCHEMY_DATABASE_URI))

target_metadata = BaseModel.metadata


def include_object(object, name, type_, reflected, compare_to):
    # Исключаем таблицы и индексы PostGIS
    excluded_tables = [
        "spatial_ref_sys",
        "topology",
        "layer",
        "county",
        "state",
        "addr",
        "edges",
        "faces",
        "county_lookup",
        "pagc_gaz",
        "zip_state_loc",
        "loader_platform",
        "cousub",
        "loader_variables",
        "featnames",
        "countysub_lookup",
        "pagc_lex",
        "street_type_lookup",
        "direction_lookup",
        "tabblock",
        "addrfeat",
        "place_lookup",
        "place",
        "zip_lookup_base",
        "tabblock20",
        "state_lookup",
        "zip_lookup_all",
        "tract",
        "pagc_rules",
        "zcta5",
        "zip_lookup",
        "loader_lookuptables",
        "geocode_settings_default",
        "geocode_settings",
        "zip_state",
        "secondary_unit_lookup",
        "bg",
        # Дополните список таблиц, которые нужно исключить
    ]
    if type_ == "table" and name in excluded_tables:
        return False
    if type_ == "index" and "gist" in name:
        return False
    return True


def do_run_migrations(connection: Connection) -> None:
    def process_revision_directives(context, revision, directives):
        script = directives[0]
        if script.upgrade_ops.is_empty():
            directives[:] = []
            logger.info("No changes found skipping revision creation.")

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        process_revision_directives=process_revision_directives,
        include_object=include_object,
        render_item=alembic_helpers.render_item,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    pass
else:
    run_migrations_online()
