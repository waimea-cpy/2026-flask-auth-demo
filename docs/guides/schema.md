# Database Schema Configuration

## Database Configuration in `app/db/config.py`

The database schema are defined in `app/db/config.py`. Each table is defined as a table class, in this format:

```python
class TableName:

    NAME = "tablename"

    SCHEMA = """
        CREATE TABLE ...
    """

    SEED_DATA = """
        INSERT INTO ...
    """
```

If no seed data is to be given for a table:

```python
    SEED_DATA = None
```

The table are then added to the `TABLES` **table registry list**, one row per table:

```python
TABLES = [
    NoteTable,
    UserTable,
    ...
]
```

*Note that the order is important - Create the tables that have foreign keys **after** the linked table has been created*


## Example Database Schema

### Schema for a Single Table

**Notes** table:

```sql
CREATE TABLE note (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    title   TEXT NOT NULL,
    body    TEXT,
    pinned  INTEGER DEFAULT 0,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Schema for Two Linked Tables

Tables are connected via **foreign keys** which link a field in one table to the **primary key** of another...

**User** table:

```sql
CREATE TABLE user (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    forename  TEXT NOT NULL,
    surname   TEXT NOT NULL,
    username  TEXT NOT NULL UNIQUE,
    pass_hash TEXT NOT NULL
)
```

**Notes** table with **foreign-key linking to user:**

```sql
CREATE TABLE note (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    title   TEXT NOT NULL,
    body    TEXT,
    pinned  INTEGER DEFAULT 0,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    user_id INTEGER NOT NULL,

    FOREIGN KEY(user_id) REFERENCES user(id)
)
```

### Schema for Two Tables with a Many-to-Many Relationship

A many-to-many relationship requires a third 'linking' table, consisting of **two foreign keys** which together also become a **composite primary key**.

Here, users can be a member of *many* clubs, and clubs can have *many* members, so a membership linking table is needed...

**User** table:

```sql
CREATE TABLE user (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    forename  TEXT NOT NULL,
    surname   TEXT NOT NULL,
    username  TEXT NOT NULL UNIQUE,
    pass_hash TEXT NOT NULL
)
```

**Club** table:

```sql
CREATE TABLE club (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    description TEXT
)
```

**Membership** table with **foreign keys to both tables**:

```sql
CREATE TABLE member (
    user_id INTEGER NOT NULL,
    club_id INTEGER NOT NULL,

    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(club_id) REFERENCES club(id),

    PRIMARY KEY(user_id, club_id)
)
```

## Seeding Tables with Sample / Test Data

You can configure each table to have sample / test data loaded into it when it is first created...

**User table seeding:**

```sql
INSERT INTO user (forename, surname, username, pass_hash)
VALUES ("Test", "User", "test", "scrypt:32768:8:1$n7eJTucLbaGmUpAM$c1776374a8d456a6eaf61bccc08db5e1fcc4ff3b3983d364c45ab13074255eeae0a393afb11f99a9fe63fb1d980992ace17a72ba70324523b11e92e36cbe4252")
```

**Notes table seeding:**

```sql
INSERT INTO note (title, body, pinned, user_id)
VALUES ("Welcome!",        "This is a demo application", 1, 1),
       ("Getting Started", "Use this template to start", 1, 1),
       ("Pinned Note",     "Pinned notes appear at top", 1, 1),
       ("Sample Note",     "This is just a sample note", 0, 1),
       ("Sample Note",     "This is just a sample note", 0, 1),
       ("Sample Note",     "This is just a sample note", 0, 1)
```

*Note that in this example, the 'test' user password is 'test'. This is a genuine hash of the password - So, you can use this to seed a user account.*


## Tips

### Table Naming

Tables should be named using **singular** names, so a table that hold notes should be called 'note'. This makes queries read a bit more logically:

- `note.id`
- `note.title`
- etc.

### Database Management Commands

A number of command-line commands are available to help you manage your database:

- `flask db-reset`  - Delete and recreate database
- `flask db-seed`   - Reseed with sample data
- `flask db-clear`  - Clear all data (with confirmation)
- `flask db-show`   - Shows the DB schema and data
- `flask db-schema` - Shows the DB schema
- `flask db-data`   - Shows the DB data

