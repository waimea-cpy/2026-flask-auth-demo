#============================================================================
# Custom Flask CLI commands for project management
#
# Provides commands:
#  - flask db-reset   Delete and recreate database
#  - flask db-seed    Reseed with sample data
#  - flask db-clear   Clear all data (with confirmation)
#  - flask db-show    Shows the DB schema and data
#  - flask db-schema  Shows the DB schema
#  - flask db-data    Shows the DB data
#============================================================================

import click
from pathlib import Path
from app.db.config import TABLES
from app.helpers.db import connect_db, _init_db_table, _seed_table, _create_db_if_needed, _log_database_schema, _log_database_data, LOCAL_DB_PATH
from app.helpers.log import get_console, get_logger

console = get_console()
logger  = get_logger()


def _confirm_action(message):
    """Prompt user to confirm a destructive action"""
    console.print(f"[red]This will {message}...[/red]")
    if not click.confirm("Are you sure?"):
        console.print("[yellow]Cancelled.[/yellow]")
        return False
    return True


def _success(table_name, action):
    console.print(f"[green]✓[/green] Table '{table_name}' {action}")

def _starting(action):
    console.rule(f"[blue bold]{action} starting...[/blue bold]", align="left")

def _complete(action):
    console.rule(f"[blue bold]{action} complete![/blue bold]", align="left")


def register_commands(app):
    """Register custom Flask CLI commands"""

    @app.cli.command('db-reset')
    def db_reset():
        """Delete and recreate the database with seed data"""
        if not _confirm_action("delete and recreate the database"):
            return

        _starting("Database reset")

        db_path = Path(LOCAL_DB_PATH)
        if db_path.exists():
            console.print(f"Deleting database: [blue]{LOCAL_DB_PATH}[/blue]")
            db_path.unlink()

        console.print("Creating fresh database...")
        _create_db_if_needed()

        console.print("Creating and seeding tables...")
        for table in TABLES:
            _init_db_table(table.NAME, table.SCHEMA, table.SEED_DATA)
            _success(table.NAME, "created and seeded")

        console.rule()
        _log_database_schema()
        console.rule()
        _log_database_data()
        _complete("Database reset")


    @app.cli.command('db-seed')
    def db_seed():
        """Reseed the database with sample data (without dropping tables)"""
        if not _confirm_action("delete all data from the database and re-seed it with sample data"):
            return

        _starting("Database seeding")

        with connect_db() as db:
            console.print("Clearing all tables...")
            for table in TABLES:
                db.execute(f"DELETE FROM {table.NAME}")
                _success(table.NAME, "cleared")

            console.print("Seeding tables with sample data...")
            for table in TABLES:
                if table.SEED_DATA:
                    _seed_table(db, logger, table.NAME, table.SEED_DATA)
                    _success(table.NAME, "re-seeded")

        console.rule()
        _log_database_data()
        _complete("Database seeding")


    @app.cli.command('db-clear')
    def db_clear():
        """Clear all data from all tables (but keep structure)"""
        if not _confirm_action("delete all existing data in the database"):
            return

        _starting("Database clearing")

        with connect_db() as db:
            console.print("Clearing all tables...")
            for table in TABLES:
                db.execute(f"DELETE FROM {table.NAME}")
                _success(table.NAME, "cleared")

        _complete("Database clearing")


    @app.cli.command('db-show')
    def db_show():
        """Display all table schema and data"""
        console.rule("[blue bold]Database Contents[/blue bold]", align="left")
        _log_database_schema()
        console.rule()
        _log_database_data()
        console.rule()


    @app.cli.command('db-schema')
    def db_show_schema():
        """Display all table schema"""
        console.rule("[blue bold]Database Schema[/blue bold]", align="left")
        _log_database_schema()
        console.rule()


    @app.cli.command('db-data')
    def db_show_data():
        """Display all table data"""
        console.rule("[blue bold]Database Data[/blue bold]", align="left")
        _log_database_data()
        console.rule()

