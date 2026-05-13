# Quick Start

## First Run

### 1. Run Rancher Desktop

Run Rancher Desktop ready to start Docker container


### 2. Configure environment vars:

Copy `.env-example` to `.env`, and edit as needed


### 3. Bring up the Docker container:

For the first time, or after editing any config files:

```bash
docker compose up --build
```

For subsequent runs:

```bash
docker compose up
```


### 4. Browse site

Visit: [http://localhost:5000](http://localhost:5000)


### 5. Shutdown the app and stop container

```bash
Ctrl+C
```

### 6. Remove the Docker container if needed

```bash
docker compose down
```


## Create Your App

### 1. Define database schema in `db/config.py`

*See [schema](schema.md) doc for more details*


### 2. Define routes and handlers in `__init__.py`

*See [CRUD example](crud.md) doc for examples*

Design Patterns to Follow...

- **Route** Pattern *(See [routes](routes.md) guide)*

  ```python
  @app.get("/path")
  def handler():
      return render_template("page.jinja")
  ```

- **Database Query** Pattern *(see [sqlite](sqlite.md) guide)*

  ```python
  with connect_db() as db:
      sql = "SELECT * FROM table WHERE col=?"
      params = (value,)
      rows = db.execute(sql, params).fetchall()
  ```

- **Form Processing** Pattern *(see [forms](forms.md) guide)*

  ```python
  @app.post("/path")
  def handler():
      value = request.form.get('field', '').strip()
      value = html.escape(value)
      # ... validate, then save
  ```


### 3. Edit / create page templates

*See [jinja](jinja.md) doc for more details*



## 😀 That's it!


