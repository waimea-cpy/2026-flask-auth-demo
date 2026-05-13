#============================================================================
# SQLite Database Setup and Logging
#============================================================================

from contextlib import contextmanager
from pathlib import Path
from dotenv import load_dotenv
from os import getenv, environ
from rich.table import Table, box
import sqlite3

from app.db.config import TABLES
from app.helpers.log import get_logger, get_console, log_prefix, truncate


load_dotenv()
LOCAL_DB_PATH = getenv("LOCAL_DB_PATH", "app/db/data.sqlite")

DB_LOGGER = "DBASE"
PREVIEW_ROWS = 3

TYPE_COLOUR = {
    "INTEGER":   "cyan",
    "REAL":      "cyan",
    "NUMERIC":   "cyan",
    "TIMESTAMP": "blue",
    "DATETIME":  "blue",
    "TEXT":      "green",
    "BLOB":      "magenta",
}

console = get_console()


def _prefix(action="", colour="blue"):
    """Helper to create database log prefix"""
    return log_prefix(action, colour, DB_LOGGER)


@contextmanager
def connect_db():
    """Create a database connection with Rich logging"""
    connection = sqlite3.connect(LOCAL_DB_PATH)
    connection.row_factory = _dict_factory

    wrapped_connection = _LoggingConnection(connection)

    try:
        yield wrapped_connection
        wrapped_connection.commit()
    except Exception:
        wrapped_connection.rollback()
        raise
    finally:
        wrapped_connection.close()


def _dict_factory(cursor, row):
    """Convert database rows to dictionaries"""
    return dict(zip([col[0] for col in cursor.description], row))


class _LoggingCursor:
    """Cursor wrapper that logs query results"""

    def __init__(self, cursor, sql_type):
        self._cursor = cursor
        self._sql_type = sql_type
        self._logger = get_logger()

    def fetchall(self):
        rows = self._cursor.fetchall()
        if self._sql_type == 'SELECT':
            self._log_rows(rows)
        return rows

    def fetchone(self):
        row = self._cursor.fetchone()
        if self._sql_type == 'SELECT':
            self._log_single_row(row)
        return row

    def _log_rows(self, rows):
        """Log multiple rows with preview"""
        num_rows = len(rows)
        self._logger.debug(
            f"{_prefix('Result')} {num_rows} {'row' if num_rows == 1 else 'rows'} returned"
        )

        if num_rows > 0:
            for row in rows[:PREVIEW_ROWS]:
                self._logger.debug(f"{_prefix()} {truncate(row)}")

            if num_rows > PREVIEW_ROWS:
                self._logger.debug(f"{_prefix()} ... and {num_rows - PREVIEW_ROWS} more")

    def _log_single_row(self, row):
        """Log a single row result"""
        row_text = "1 row" if row else "0 rows"
        self._logger.debug(f"{_prefix('Result')} {row_text} returned")

        if row:
            self._logger.debug(f"{_prefix()} {truncate(row)}")

    def __getattr__(self, name):
        return getattr(self._cursor, name)


class _LoggingConnection:
    """Connection wrapper that logs all database operations"""

    def __init__(self, conn):
        self._conn = conn
        self._logger = get_logger()

    def execute(self, sql, params=(), logged=True):
        """Execute a single SQL statement with logging"""
        try:
            if logged:
                collapsed_sql = ' '.join(sql.split())
                self._log_query(collapsed_sql, params)

            cursor = self._conn.execute(sql, params)

            if logged:
                if self._is_select(sql):
                    return _LoggingCursor(cursor, 'SELECT')

                self._log_mutation_result(sql, cursor.rowcount, cursor.lastrowid)

            return cursor

        except sqlite3.Error as e:
            self._log_error(e, sql, params)
            raise

    def executemany(self, sql, params):
        """Execute SQL with multiple parameter sets"""
        try:
            collapsed_sql = ' '.join(sql.split())
            params_list = list(params)
            num_rows = len(params_list)

            self._log_query(collapsed_sql, f"{num_rows} row{'s' if num_rows != 1 else ''}")

            cursor = self._conn.executemany(sql, params_list)
            self._log_mutation_result(sql, cursor.rowcount, cursor.lastrowid)

            return cursor

        except sqlite3.Error as e:
            self._log_error(e, sql, f"{num_rows} rows")
            raise

    def _is_select(self, sql):
        """Check if SQL is a SELECT statement"""
        return sql.strip().upper().startswith('SELECT')

    def _log_query(self, sql, params):
        """Log the query being executed"""
        self._logger.debug(f"{_prefix('Query')} {sql}")
        self._logger.debug(f"{_prefix('Params')} {params}")

    def _log_mutation_result(self, sql, rowcount, lastrowid):
        """Log the result of INSERT/UPDATE/DELETE"""
        sql_upper = sql.upper()
        row_text = f"{rowcount} row{'s' if rowcount != 1 else ''}"

        if sql_upper.startswith('INSERT'):
            self._logger.debug(f"{_prefix('Result')} {row_text} inserted [dim](ID: {lastrowid})[/dim]")
        elif sql_upper.startswith('UPDATE'):
            self._logger.debug(f"{_prefix('Result')} {row_text} updated")
        elif sql_upper.startswith('DELETE'):
            self._logger.debug(f"{_prefix('Result')} {row_text} deleted")
        else:
            self._logger.debug(f"{_prefix('Result')} {row_text} affected")

    def _log_error(self, error, sql=None, params=None):
        """Log database errors"""
        self._logger.error(f"{_prefix('Error', 'red bold')} {error}")
        if sql:
            self._logger.error(f"{_prefix('Query', 'red')} {sql}")
        if params:
            self._logger.error(f"{_prefix('Params', 'red')} {params}")

    def commit(self):
        return self._conn.commit()

    def rollback(self):
        return self._conn.rollback()

    def close(self):
        return self._conn.close()

    def __getattr__(self, name):
        return getattr(self._conn, name)


def init_database():
    """Initialize database with all configured tables"""

    # Only run on main process (not reloader parent)
    if environ.get('WERKZEUG_RUN_MAIN') != 'true':
        return

    console = get_console()
    console.rule("[blue bold]Database Configuration[/blue bold]")

    _create_db_if_needed()

    for table in TABLES:
        _init_db_table(table.NAME, table.SCHEMA, table.SEED_DATA)

    _log_database_schema()
    console.rule()
    _log_database_data()


def _create_db_if_needed():
    """Initialize database - ensure directory exists"""
    db_path = Path(LOCAL_DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)


def _init_db_table(table_name, schema, seed_sql):
    """Initialize a database table with schema and seed data"""
    with connect_db() as db:
        if _table_exists(db, table_name):
            return

        logger = get_logger()
        logger.info(f"{_prefix('Table', 'cyan')} creating '{table_name}'...")

        db.execute(schema)

        if seed_sql:
            _seed_table(db, logger, table_name, seed_sql)


def _table_exists(db, table_name):
    """Check if a table exists in the database"""
    result = db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,),
        logged=False
    ).fetchone()
    return result is not None


def _seed_table(db, logger, table_name, seed_sql):
    """Seed a table with initial data"""
    logger.info(f"{_prefix('Table', 'cyan')} seeding '{table_name}' with data")
    db.execute(seed_sql)
    logger.info(f"{_prefix('Table', 'cyan')} '{table_name}' seeded with data")


def _log_database_schema():
    """Log comprehensive database schema information"""

    with connect_db() as db:
        tables = db.execute("""
            SELECT type, name, tbl_name, sql
            FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """, logged=False).fetchall()

        if not tables:
            return

        for table in tables:
            table_name = table['name']
            table_sql  = table['sql'] or ''

            columns      = db.execute(f"PRAGMA table_info({table_name})",       logged=False).fetchall()
            foreign_keys = db.execute(f"PRAGMA foreign_key_list({table_name})", logged=False).fetchall()
            indexes      = db.execute(f"PRAGMA index_list({table_name})",       logged=False).fetchall()

            col_table = Table(
                title=f"[blue bold]{table_name}[/blue bold] table schema",
                # show_header=False,
                title_justify="left",
                header_style="white italic",
                box=box.ROUNDED,
            )
            col_table.add_column("Key",        style="green")
            col_table.add_column("Column",     style="yellow")
            col_table.add_column("Data Type",  style="cyan")
            col_table.add_column("Constraints")
            if foreign_keys:
                col_table.add_column("References")

            for col in columns:
                constraints = []
                keys = ""
                refs = ""

                if col['pk']:
                    keys = "PK"
                    if col['type'].upper() == 'INTEGER' and 'AUTOINCREMENT' in table_sql.upper():
                        constraints.append('AUTOINCREMENT')

                if foreign_keys:
                    for fk in foreign_keys:
                        if col['name'] == fk['from']:
                            keys += " " if keys else ""
                            keys += "[magenta]FK[/magenta]"
                            refs = f"[magenta]FK[/magenta] ➜ [blue]{fk['table']}[/blue]([yellow]{fk['to']}[/yellow])"

                if col['notnull']:
                    constraints.append('NOT NULL')

                if col['dflt_value']:
                    constraints.append(f"DEFAULT {col['dflt_value']}")

                if indexes:
                    for idx in indexes:
                        if idx['unique']:
                            idx_info = db.execute(f"PRAGMA index_info({idx['name']})", logged=False).fetchall()
                            idx_columns = [idx_col['name'] for idx_col in idx_info]
                            # Only mark as UNIQUE if this is a single-column index on this column
                            if len(idx_columns) == 1 and col['name'] in idx_columns:
                                constraints.append('[green]UNIQUE[/green]')

                cons = ', '.join(constraints) if constraints else ''

                if refs:
                    col_table.add_row(keys, col['name'], col['type'] or '', cons, refs)
                else:
                    col_table.add_row(keys, col['name'], col['type'] or '', cons)

            console.print(col_table)


def _log_database_data():
    """Log database table data in a compact table format"""

    with connect_db() as db:
        tables = db.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """, logged=False).fetchall()

        if not tables:
            return

        for table_info in tables:
            table_name = table_info['name']
            rows    = db.execute(f"SELECT * FROM {table_name}",      logged=False).fetchall()
            columns = db.execute(f"PRAGMA table_info({table_name})", logged=False).fetchall()

            col_names = [col['name'] for col in columns]
            col_types = {col['name']: col['type'].upper() for col in columns}

            # Create Rich table
            data_table = Table(
                title=f"[blue bold]{table_name}[/blue bold] table data: [dim]({len(rows)} rows)[/dim]",
                title_justify="left",
                show_lines=True,
                header_style="yellow italic",
                box=box.ROUNDED,
                min_width=30,
            )

            # Add columns
            for col_name in col_names:
                data_table.add_column(
                    col_name,
                    overflow="ellipsis",
                )

            # Add rows
            for row in rows:
                row_data = []
                for col_name in col_names:
                    value = row[col_name]

                    if value is None:
                        value = "NULL"
                        colour = "dim"
                    else:
                        type = col_types.get(col_name, '')
                        colour = TYPE_COLOUR.get(type, 'white')
                        if type == "TEXT":
                            value = str(value).replace('\n', '[yellow]\\n[/yellow]')
                            value = f'"{value}"'
                        elif type == "BLOB":
                            value = f"<BLOB {len(value)} bytes>"

                    row_data.append(f"[{colour}]{value}[/{colour}]")

                data_table.add_row(*row_data)

            console.print(data_table)

