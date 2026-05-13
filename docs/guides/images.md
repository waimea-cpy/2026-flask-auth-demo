# Image / File Uploading and Access

If you are dealing withe relatively small images / files (100kB or less), then you can store these directly in the database as **Binary Large OBject (BLOB)** data.

*(If you are storing larger files / images, database BLOBs would result in a very large SQLite database file. In this case, you should **upload the files to a storage location** and only **store a reference to the location in the DB**. However, this is outside the scope of this guide)*


## Setup the Database

Define the DB schema with a **BLOB** field, and in the case of images, you will need to store the **[MIME type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types/Common_types)** to identify the image type when accessing it...

```sql
CREATE TABLE club (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT NOT NULL,
    logo_data BLOB NOT NULL,
    logo_mime TEXT NOT NULL
)
```

## Setup forms to allow file uploads

If a form is uploading images / files, it needs to be a `multipart` form.

In addition, the file input control should specify the type(s) of file that can be uploaded using the `accept` parameter. Examples:
- **PNG** images only: `"image/png"`
- **Common image** types: `"image/png, image/jpeg, image/gif, image/webp"`
- **All image** types: `"image/*"`
- **Text** files only: `".txt"`
- **Word** files only: `".docx"`


```html
<form method="post" action="/club" enctype="multipart/form-data">
    <label>
        Name
        <input name="name" type="text" required>
    </label>

    <label>
        Logo
        <input
            name="logo"
            type="file"
            accept="image/png, image/jpeg, image/gif, image/webp"
            required
        >
    </label>

    <button>Add Club</button>
</form>
```

## Setup a form processing route and function

Most data submitted by a form is accessed via `request.form.get(...)`. The uploaded image / file data is handled separately from the other form data values, coming via `request.files.get(...)`...

```python
@app.post("/club")
def add_club():
    name = request.form.get('name', '').strip()
    name = html.escape(name)

    logo = request.files.get('logo', None)
    if not logo:
        flash("There was a problem uploading the image", "error")
        return redirect("/")

    logo_data = logo.read()
    logo_mime = logo.mimetype

    with connect_db() as db:
        sql = """
            INSERT INTO club (name, logo_data, logo_mime)
            VALUES (?, ?, ?)
        """
        params = (name, logo_data, logo_mime)
        db.execute(sql, params)

        flash(f"Club '{name}' added", "success")
        return redirect("/")
```

## Serve uploaded images using `<img>`

When accessing database entries, **do not request the image data** along with other data values. Instead, **use a separate HTTP request for the image data via an `<img>` tag** on the page you want to show the image, and provide a dedicated route for this...

### 1. Get data for the page (but *not* the image)

```python
@app.get('/club/<int:id>')
def get_club(id):
    with connect_db() as db:
        sql = "SELECT name FROM club WHERE id=?"
        params = (id,)
        club = db.execute(sql, params).fetchone()

        return render_template("pages/club.jinja", club=club)
```

### 2. Template to show data with an `<img>` tag

The source of the image is set to a special image loading route, `/club/{{ club.id }}/logo`...

```jinja
{% raw %}{# Show the club info and request image... #}

<h1>Welcome to '{{ club.name }}' Club!</h1>

<img src="/club/{{ club.id }}/logo" alt="{{ club.name }} logo">    {% endraw %}
```
<!-- Ignore the `raw` and `endraw` tags in these Jinja code snippets - they are required for GitHub Pages -->

### 3. Route to serve up the image

This route retrieves the image data and MIME type, then creates an image file and returns this...

```python
@app.get('/club/<int:id>/logo')
def get_club_logo(id):
    with connect_db() as db:
        sql = "SELECT logo_data, logo_mime FROM club WHERE id=?"
        params = (id,)
        logo = db.execute(sql, params).fetchone()

        if not logo:
            return render_template("pages/404.jinja"), 404

        return make_response(
            send_file(
                BytesIO(logo["logo_data"]),
                mimetype=logo["logo_mime"]
            )
        )
```

*Using a separate HTTP request allows the browser to load and render the page without having to wait for the image data to load (which could take a while)*


## Provide Download Links for Uploaded Files

If you have allowed files such as `.txt` to be uploaded, you might want to allow these to be downloaded later via a route...

```python
@app.get('/club/<int:id>/info/download')
def download_club_info(id):
    with connect_db() as db:
        sql = "SELECT name, info_doc_data FROM club WHERE id=?"
        params = (id,)
        club = db.execute(sql, params).fetchone()

        if not club or not club["info_doc_data"]:
            return render_template("pages/404.jinja"), 404

        return send_file(
            BytesIO(club["info_doc_data"]),
            mimetype="text/plain",
            download_name=f"{club['name']}-info.txt",
            as_attachment=True
        )
```

