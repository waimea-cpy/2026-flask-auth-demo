# Flask App Setup

The app uses a **Docker container** to setup and configure Python ready for use, install all required libraries, etc.

Some configuration is needed before creating and starting the container...


## Configure Environment:

   Setup the environment variable file that define key values for the app...

   Copy `.env.example` to `.env`

   Customize `.env` if needed. At the least, change the secret string (used to encrypt session cookies)


## Setup the Database

### 1. Define Database Schema and Seed Data:

   Modify `app/db/config.py` to change database schema and define sample seed data.

   Database schema examples can be found in [schema.md](schema.md)

### 2. Create Database:

   The database is automatically created and seeded on **first run**...


## Bring up the Docker container to Launch the App

### 1. Launch Rancher Desktop:

Rancher Desktop provides the back-end for setting up and running Docker containers. It needs to be running before you begin.


### 2. Bring up the container:

   In a terminal, if this is the first time...

   ```bash
   docker compose up --build
   ```

   If the config has not changed...

   ```bash
   docker compose up
   ```


### 2. View in browser:

   Open [http://localhost:5000](http://localhost:5000) in a browser


### 3. View Logs:

   Watch the console to see **logs** for:
   - Database configuration
   - HTTP requests and responses
   - SQL queries and results
   - Traceback of errors


### 5. Shutdown the app and stop container

  In a terminal...

  ```bash
  Ctrl+C
  ```

  If you want to completely remove the container...

  ```bash
  docker compose down
  ```


## Command-Line DB Management Commands

A number of command-line commands are available to help you manage your database. In a *separate terminal window* to the one running the app...

```bash
docker compose exec web flask db-reset   # Delete and recreate database
docker compose exec web flask db-seed    # Reseed with sample data
docker compose exec web flask db-clear   # Clear all data (with confirmation)
docker compose exec web flask db-show    # Shows the DB schema and data
docker compose exec web flask db-schema  # Shows the DB schema
docker compose exec web flask db-data    # Shows the DB data
```
