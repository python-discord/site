import importlib
import json
import os
from typing import Callable

from pysite.database import RethinkDB
from pysite.tables import TABLES

TABLES_DIR = os.path.abspath("./pysite/migrations/tables")
VERSIONS_TABLE = "_versions"


def get_migrations(table_path, table):
    """
    Take a table name and the path to its migration files, and return a dict containing versions and modules
    corresponding with each migration.

    And, yes, migrations start at 1.
    """
    migrations = {}
    final_version = 0

    for filename in os.listdir(table_path):
        if filename.startswith("v") and filename.endswith(".py"):
            final_version = int(filename[1:-3])
            migrations[final_version] = f"pysite.migrations.tables.{table}.v{final_version}"

    return dict(sorted(migrations.items())), final_version


def run_migrations(db: RethinkDB, output: Callable[[str], None]=None):
    for table, obj in TABLES.items():  # All _defined_ tables
        table_path = os.path.join(TABLES_DIR, table)

        if not os.path.exists(table_path):  # Check whether we actually have any migration data for this table at all
            output(f"No migration data found for table: {table}")
            continue

        with db.get_connection() as conn:  # Make sure we have an active connection
            try:
                if not db.query(table).count().run(conn):  # If there are no documents in the table...
                    # Table's empty, so we'll have to run migrations again anyway
                    db.delete(VERSIONS_TABLE, table)

                    json_path = os.path.join(table_path, "initial_data.json")

                    if os.path.exists(json_path):  # We have initial data to insert, so let's do that
                        with open(json_path, "r", encoding="utf-8") as json_file:
                            data = json.load(json_file)
                            db.insert(table, *data)  # Table's empty, so... just do the thing

                            output(f"Inserted initial data for table: {table}")
                    else:  # There's no json data file for this table
                        output(f"No initial_data.json file for table: {table}")
                        output(json_path)

                # Translate migration files into modules and versions
                migrations, final_version = get_migrations(table_path, table)

                if not migrations:  # No migration files found
                    output(f"No structural migrations for table: {table}")
                    continue

                current_version = 0
                doc = db.get(VERSIONS_TABLE, table)

                if doc:  # We've done a migration before, so continue from where we left off
                    current_version = doc["version"]

                    if current_version == final_version:  # Nothing to do, we're up to date
                        output(f"Table is already up to date: {table}")
                        continue
                    output(f"Table has never been migrated: {table}")

                while current_version < final_version:
                    current_version += 1

                    module = importlib.import_module(migrations[current_version])
                    module.run(db, table, obj)
                    output(f"Table upgraded to version {current_version}/{final_version}: {table}")

                    # Make sure the versions table is kept up to date, so we don't ever migrate twice
                    # We do this in the loop to save our progress, in case we fail during a migration

                    db.insert(
                        VERSIONS_TABLE,
                        {"table": table, "version": current_version},
                        conflict="replace",
                        durability="soft"
                    )
            except Exception as e:
                # TODO: Should this fail hard and just raise?
                output(f"Failed to migrate table: {table} - {e}")
            finally:
                db.sync(VERSIONS_TABLE)
