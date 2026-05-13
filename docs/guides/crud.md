# Example of a Simple Flask CRUD App

A simple Flask / SQLite / Jinja app with routes to: **C**reate, **R**ead, **U**pdate, **D**elete data.


## App Configuration

### DB Schema

```SQL
CREATE TABLE note (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    title   TEXT NOT NULL,
    body    TEXT,
    pinned  INTEGER DEFAULT 0,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### App Routes

| Method | Route                   | Description           |
| ------ | ----------------------- | --------------------- |
| `GET`  | `/`                     | list all notes (home) |
| `GET`  | `/note/<int:id>`        | show a single note    |
| `GET`  | `/note/new`             | new note form         |
| `POST` | `/note`                 | add a new note        |
| `GET`  | `/note/<int:id>/edit`   | not edit form         |
| `POST` | `/note/<int:id>`        | update a note         |
| `GET`  | `/note/<int:id>/delete` | delete a note         |


### App Templates

| Name                   | Data Needed | Description                  |
| ---------------------- | ----------- | ---------------------------- |
| `note_list.jinja`      | `notes[]`   | Show a list of all notes     |
| `note_single.jinja`    | `note`      | Show a single note in detail |
| `note_form.jinja`      |             | Show a new note form         |
| `note_form_edit.jinja` | `note`      | Show a note edit form        |


## Routes and Handlers

### Reading Notes

```python
# Show all notes -------------------------------------------
@app.get("/")
def show_notes():
    with connect_db() as db:
        sql = """
            SELECT id, title, body, pinned, created
            FROM note
            ORDER BY pinned DESC, created DESC
        """
        params = ()
        notes = db.execute(sql, params).fetchall()

        return render_template("pages/note_list.jinja", notes=notes)


# Show a single note ----------------------------------------
@app.get("/note/<int:id>")
def show_a_note(id):
    with connect_db() as db:
        sql = """
            SELECT id, title, body, pinned, created
            FROM note
            WHERE id=?
        """
        params = (id,)
        note = db.execute(sql, params).fetchone()

        return render_template("pages/note_single.jinja", note=note)
```

### Creating Notes

```python
# Show new note form ----------------------------------------
@app.get("/note/new")
def show_note_form():
    return render_template("pages/note_form.jinja")


# Process new note ------------------------------------------
@app.post("/note")
def add_a_note():
    title = request.form.get('title', '').strip()
    body = request.form.get('body', '').strip()

    pinned = bool(request.form.get('pin'))

    title = html.escape(title)
    body = html.escape(body)

    with connect_db() as db:
        sql = """
            INSERT INTO note (title, body, pinned)
            VALUES (?, ?, ?)
        """
        params = (title, body, pinned)
        db.execute(sql, params)

        flash("Note added", "success")
        return redirect("/")
```

### Updating Notes

```python
# Show note edit form with existing data --------------------
@app.get("/note/<int:id>/edit")
def show_note_edit_form(id):
    with connect_db() as db:
        sql = """
            SELECT id, title, body, pinned, created
            FROM note
            WHERE id=?
        """
        params = (id,)
        note = db.execute(sql, params).fetchone()

        return render_template("pages/note_form_edit.jinja", note=note)


# Process updated note --------------------------------------
@app.post("/note/<int:id>")
def update_a_note(id):
    title = request.form.get('title', '').strip()
    body = request.form.get('body', '').strip()

    pinned = bool(request.form.get('pin'))

    title = html.escape(title)
    body = html.escape(body)

    with connect_db() as db:
        sql = """
            UPDATE note
            SET title=?, body=?, pinned=?
            WHERE id=?
        """
        params = (title, body, pinned, id)
        db.execute(sql, params)

        flash("Note updated", "success")
        return redirect("/")
```

### Deleting Notes

```python
# Delete a note ---------------------------------------------
@app.get("/note/<int:id>/delete")
def delete_a_note(id):
    with connect_db() as db:
        sql = """
            DELETE FROM note
            WHERE id=?
        """
        params = (id,)
        db.execute(sql, params)

        flash("Note deleted", "success")
        return redirect("/")
```


## Jinja Templates

### notes_list.jinja

```jinja
{% raw %}{% block content %}

    <section class="notes">
        {% for note in notes %}

            <article class="note {{ 'pinned' if note.pinned }}">

                <header>
                    <h3>{{ note.title }}</h3>
                    {{ "📌" if note.pinned }}
                </header>

                <p><a href="/note/{{ note.id }}">View note...</a></p>

            </article>

        {% else %}

            <p>No Notes!</p>

        {% endfor %}
    </section>

{% endblock %}  {% endraw %}
```

### note_single.jinja

```jinja
{% raw %}{% block content %}

<article class="note {{ 'pinned' if note.pinned }}">

    <header>
        <h3>{{ note.title }}</h3>
        {{ "📌" if note.pinned }}
    </header>

    <p>{{ note.body | paragraphs }}</p>

    <footer>
        <span>Created on {{ note.created | local | format }}</span>

        <span><a href="/note/{{ note.id }}/edit">🖊️ Edit</a></span>
        <span><a href="/note/{{ note.id }}/delete"
                 onclick="return confirm('Really delete?')">🗑 Delete</a></span>
    </footer>

</article>

{% endblock %}  {% endraw %}
```

### note_form.jinja

```jinja
{% raw %}{% block content %}

<article>

    <form method="post" action="/note">
        <h3>New Note</h3>

        <label>
            Title
            <input name="title" type="text" required>
        </label>

        <label>
            Body
            <textarea name="body" required></textarea>
        </label>

        <label>
            <input name="pin" type="checkbox">
            Pin note?
        </label>

        <button>Add Note</button>
    </form>

</article>

{% endblock %}  {% endraw %}
```

### note_form_edit.jinja

```jinja
{% raw %}{% block content %}

<article>

    <form method="post" action="/note/{{ note.id }}">
        <h3>Edit Note</h3>

        <label>
            Title
            <input name="title" type="text" value="{{ note.title }}" required>
        </label>

        <label>
            Body
            <textarea name="body" required>{{ note.body }}</textarea>
        </label>

        <label>
            <input name="pin" type="checkbox" {{ 'checked' if note.pinned }}>
            Pin note?
        </label>

        <button>Update Note</button>
    </form>

</article>

{% endblock %}  {% endraw %}
```
