# User Authentication

## Simple Authentication without a User Table

If you just need a very simple authentication scheme to limit access to parts of your site (e.g. for an admin page), you can use just a password...


### 1. Add a password to your `.env` file

```bash
ADMIN_PASSWORD=secret
```

### 2. Create a login form page

Serve this up from `/login` route...

```html
<form method="post" action="/login">
    <label>
        Password
        <input name="password" type="password" required>
    </label>

    <button>Login</button>
</form>
```

### 3. Create a login POST route

This loads the password from the `.env` file and compares it with the entered one...

```python
@app.post("/login")
def login_admin():
    password = request.form.get('password', '').strip()

    load_dotenv()
    ADMIN_PASSWORD = getenv("ADMIN_PASSWORD", "")
    if not ADMIN_PASSWORD:
        flash(f"No admin password set!", "error")
        return redirect("/")

    if password == ADMIN_PASSWORD:
        session["logged_in"] = True
        flash(f"Login successful", "success")
        return redirect("/")
    else:
        session.clear()
        flash(f"Incorrect password", "error")
        return redirect("/")
```

### 4. Add the `@login_required` decorator to required routes

```python
@app.get("/admin")
@login_required
def admin_page():
    # Can only access this route if logged in
    ...
```

### 5. Create a logout route

```python
@app.get("/logout")
def logout_admin():
    session.clear()
    flash(f"You have been logged out", "success")
    return redirect("/")
```

### 6. Show admin / non-admin nav links

Update the nav menu in `templates/pages/base.jinja`...

```jinja
{% raw %}{# Show different options depending on login state... #}

{% if session.logged_in %}
    <li>Welcome, Admin!</li>
    <li><a href="/admin">Admin</a></li>
    <li><a href="/logout">Logout</a></li>
{% else %}
    <li><a href="/login">Login</a></li>
{% endif %}     {% endraw %}
```
<!-- Ignore the `raw` and `endraw` tags in these Jinja code snippets - they are required for GitHub Pages -->


## User Authentication with User Account Table

If you need to create multiple user accounts and authenticate them based on username and password, you will need a dedicated `user` table in your database.

*Note: Best practice is to **never store user passwords** in your database, but instead to store a **hash** of the password*

### 1. Create a 'user' table

```sql
CREATE TABLE user (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    forename  TEXT NOT NULL,
    surname   TEXT NOT NULL,
    username  TEXT NOT NULL UNIQUE,
    pass_hash TEXT NOT NULL
)
```

### 2. Create a sign-up form

Serve this from a `/user/new` route, or similar...

```html
<form method="post" action="/user">
    <label>
        Forename
        <input name="forename" type="text" required>
    </label>

    <label>
        Surname
        <input name="surname" type="text" required>
    </label>

    <label>
        Username
        <input name="username" type="text" required>
    </label>

    <label>
        Password
        <input name="password" type="password" required>
    </label>

    <button>Sign Up</button>
</form>
```

### 3. Create a user POST route

Once this is in place, you should be able to create user accounts

```python
@app.post("/user")
def add_user():
    forename = request.form.get('forename', '').strip()
    surname  = request.form.get('surname',  '').strip()
    username = request.form.get('username', '').strip().lower()
    password = request.form.get('password', '').strip()

    with connect_db() as db:
        sql = "SELECT id FROM user WHERE username=?"
        params = (username,)
        user = db.execute(sql, params).fetchone()

        if user:
            flash(f"Username '{username}' already exists", "error")
            return redirect("/user/new")

        pass_hash = generate_password_hash(password)

        sql = """
            INSERT INTO user (forename, surname, username, pass_hash)
            VALUES (?, ?, ?, ?)
        """
        params = (forename, surname, username, pass_hash)
        db.execute(sql, params)

        flash("Account created. Please login", "success")
        return redirect("/login")
```

### 4. Create a login form page

Serve this up from `/login` route...

```html
<form method="post" action="/login">
    <label>
        Username
        <input name="username" type="text" required>
    </label>

    <label>
        Password
        <input name="password" type="password" required>
    </label>

    <button>Login</button>
</form>
```

### 5. Create a login POST route

This loads the password from the `.env` file and compares it with the entered one...

```python
@app.post("/login")
def login_user():
    username = request.form.get('username', '').strip().lower()
    password = request.form.get('password', '').strip()

    with connect_db() as db:
        sql = """
            SELECT id, forename, surname, pass_hash
            FROM user
            WHERE username=?
        """
        params = (username,)
        user = db.execute(sql, params).fetchone()

        if not user:
            flash(f"Unknown user", "error")
            return redirect("/login")

        if not check_password_hash(user["pass_hash"], password):
            flash(f"Incorrect password", "error")
            return redirect("/login")

        session["logged_in"] = True
        session["user"] = {
            "username": username,
            "forename": user["forename"],
            "surname":  user["surname"],
        }

        flash("Login successful", "success")
        return redirect("/")
```

### 6. Add the `@login_required` decorator to required routes

```python
@app.get("/admin")
@login_required
def admin_page():
    # Can only access this route if logged in
    ...
```

### 7. Create a logout route

```python
@app.get("/logout")
def logout_admin():
    session.clear()
    flash(f"You have been logged out", "success")
    return redirect("/")
```

### 8. Show admin / non-admin nav links

Update the nav menu in `templates/pages/base.jinja`...

```jinja
{% raw %}{# Show different options depending on login state... #}

{% if session.logged_in %}
    <li>Welcome, {{ session.user.forename }}!</li>
    <li><a href="/admin">Admin</a></li>
    <li><a href="/logout">Logout</a></li>
{% else %}
    <li><a href="/login">Login</a></li>
    <li><a href="/user/new">Sign-Up</a></li>
{% endif %}     {% endraw %}
```
<!-- Ignore the `raw` and `endraw` tags in these Jinja code snippets - they are required for GitHub Pages -->

### 9. Use the logged-in user info. when required

If you need to know the logged in user information (e.g. you need the ID when posting a new DB record linked to the user), you can get this from `session["user"]`...

```python
with connect_db() as db:
    user_id = session["user"]["id"]
    sql = """
        INSERT INTO note (title, body, user_id)
        VALUES (?, ?, ?)
    """
    params = (title, body, user_id)
    db.execute(sql, params)
```

Or in a Jinja template (using the 'dot' syntax)...

```jinja
{% raw %}{# Show logged in user name... #}

{% if session.logged_in %}
    <p>Welcome, {{ session.user.forename }}!</p>
{% endif %}     {% endraw %}
```
<!-- Ignore the `raw` and `endraw` tags in these Jinja code snippets - they are required for GitHub Pages -->
