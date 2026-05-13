# Flask Route Handling

## Naming Routes

Try to be consistent when naming routes. A good pattern to use is:

**Fetching Data:**
- `GET  /notes` - for a page that has multiple items
- `GET  /note/<int:id>` - for a page that shows a single thing by ID
- `GET  /notes/pinned` - for a page that has multiple, specific items

**New Data:**
- `GET  /note/new` - for a page with a form for a new item
- `POST /note` - to process the new item form data

**Updating Data:**
- `GET  /note/<int:id>/edit` - for a page with a form to edit an item
- `POST /note/<int:id>` - to process updated data for an item

**Deleting Data:**
- `GET  /note/<int:id>/delete` - to process an item deletion

*Note: within routes, **numeric** parameters use `<int:value>`, whilst **text** parameters use `<value>`*


## Defining Routes

### Route to Show a Static Page (No DB Data)

```python
@app.get("/about")
def example_route():
    return render_template("pages/about.jinja")
```

```python
@app.get("/note/new")
def example_route():
    return render_template("pages/note_form.jinja")
```

### Route to Show All DB Items

```python
@app.get("/notes")
def show_note_list():
    with connect_db() as db:
        sql = "SELECT * FROM note"
        notes = db.execute(sql).fetchall()
    return render_template("pages/note_list.jinja", notes=notes)
```

### Route to Show a Specific Group of DB Items

The route can specify a particular set of items, e.g. all pinned notes...

```python
@app.get("/notes/pinned")
def show_pinned_note_list():
    with connect_db() as db:
        sql = "SELECT * FROM note WHERE pinned=1"
        notes = db.execute(sql).fetchall()
    return render_template("pages/note_list.jinja", notes=notes, title="Pinned Notes")
```

### Route to Show a DB Item(s) Matching a Parameter

The route can contain a parameter, `<...>`, which can be passed into the handler function and then used in the DB query...

#### Single item, e.g. a note with a specific ID, `<int:id>`:

```python
@app.get("/note/<int:id>")
def show_note(id):
    with connect_db() as db:
        sql = "SELECT * FROM note WHERE id=?"
        params = (id,)
        note = db.execute(sql, params).fetchone()
    return render_template("pages/note_info.jinja", note=note)
```

#### Multiple items, e.g. notes in a given category, `<category>`:

```python
@app.get("/notes/<category>")
def show_note(category):
    with connect_db() as db:
        sql = "SELECT * FROM note WHERE category=?"
        params = (category,)
        note = db.execute(sql, params).fetchone()
    return render_template("pages/note_info.jinja", note=note)
```

### Protected Routes - Authorised Users Only

Add the `@login_required` decorator to stop routes being accessed by unauthorised users...

```python
@app.get("/admin")
@login_required
def admin_page():
    # Only accessible if session['logged_in'] is True
    return render_template("pages/admin.jinja")
```

### Route for a Search Query

A search form, using the `GET` method...

```html
<form method="GET" action="/notes/search">
    <input name="query" type="text" required>
    <button>Search Notes</button>
</form>
```

... would result in an HTTP request URL of the form `/notes/search?query=...` which is then matched and handled, using the search term in a wild-card DB query...

*Note: In SQL, `%` means **match anything**, so adding `%` either side of the search term results in a query where the search terms can appear anywhere in the text - a **wild-card** search*

```python
@app.get("/notes/search")
def search_notes():
    # Get search query and add wildcards
    search = request.args.get('query')
    search = f"%{search}%"

    with connect_db() as db:
        sql = """
            SELECT * FROM note
            WHERE title LIKE ? OR body LIKE ?
        """
        params = (search, search)
        notes = db.execute(sql, params).fetchall()

    return render_template("pages/note_list.jinja", notes=notes,
                           title=f"Notes matching '{query}'")
```

## Route Redirects

Immediately loads a different route...

```python
return redirect("/")
return redirect(f"/note/{id}")
```

