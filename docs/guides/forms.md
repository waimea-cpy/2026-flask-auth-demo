# Handling Form Data

## Typical Form with a Range of Inputs

```html
<form method="post" action="/note">
    <h3>New Note</h3>

    <label>
        Title
        <input name="title" type="text" placeholder="e.g. Feed cat" required>
    </label>

    <label>
        Body
        <textarea name="body" placeholder="e.g. Two scoops" required></textarea>
    </label>

    <label>
        <input name="pin" type="checkbox">
        Pin note?
    </label>

    <label>
        Category
        <select name="category">
            <option>Personal<option>
            <option>Family<option>
            <option>Work<option>
        </select>
    </label>

    <fieldset>
        <legend>Priority</legend>
        <label><input name="priority" value="5" type="radio"> 5</label>
        <label><input name="priority" value="4" type="radio"> 4</label>
        <label><input name="priority" value="3" type="radio" checked> 3</label>
        <label><input name="priority" value="2" type="radio"> 2</label>
        <label><input name="priority" value="1" type="radio"> 1</label>
    </fieldset>

    <fieldset>
        <legend>Tags</legend>
        <label><input name="tags" value="todo" type="checkbox"> todo</label>
        <label><input name="tags" value="call" type="checkbox"> call</label>
        <label><input name="tags" value="shop" type="checkbox"> shop</label>
    </fieldset>

    <button>Add Note</button>
</form>
```
Giving this form...

<form id="formdemo" method="post" action="/note">
  <h3>New Note</h3>
  <label>Title <input name="title" type="text" placeholder="e.g. Feed cat" required></label>
  <label>Body <textarea name="body" required placeholder="e.g. Two scoops"></textarea></label>
  <label><input name="pin" type="checkbox"> Pin note?</label>
  <label>Category <select name="category">
    <option>Personal</option>
    <option>Family</option>
    <option>Work</option>
  </select></label>
  <fieldset>
    <legend>Priority</legend>
    <label><input name="priority" value="5" type="radio"> 5</label>
    <label><input name="priority" value="4" type="radio"> 4</label>
    <label><input name="priority" value="3" type="radio" checked> 3</label>
    <label><input name="priority" value="2" type="radio"> 2</label>
    <label><input name="priority" value="1" type="radio"> 1</label>
  </fieldset>
  <fieldset>
    <legend>Tags</legend>
    <label><input name="tags" value="todo" type="checkbox"> home</label>
    <label><input name="tags" value="call" type="checkbox"> call</label>
    <label><input name="tags" value="shop" type="checkbox"> shop</label>
  </fieldset>
  <button>Add Note</button>
</form>

## Get Values from Form

Get form data via `request.form.get('key').strip()`...
- `.get('key')` gets the form input with the name 'key'
- `.get('key', '')` value will be nothing if the input missing
- `.strip()` removes leading / trailing spaces
- Can also add other text transforms: `.lower()`, `.upper()`, etc.

```python
# Get form text data
title = request.form.get('title', '').strip()
body = request.form.get('body', '').strip()

# Get radio button value
priority = request.form.get('priority')

# Get checkbox state as a boolean
pinned = bool(request.form.get('pin'))   # True/False

# Get all values from checkboxes / selects
tag_list = request.form.getlist('tags')  # ['todo', 'shop']
tags = ", ".join(tag_list)               # "todo, shop"
```


## Escaping Text Values to Avoid XSS

**Always** escape text input values *(see security note below)*

```python
# Escape text to avoid XSS exploits
title = html.escape(title)
body = html.escape(body)
```


## Validation of Input Data

Check that a value is **present**:

```python
title = request.form.get('title', '').strip()

if not title:
    flash("Title is required", "error")
    return redirect("/note/new")
```

### Text Values

Check that a text value is **not too long**:

```python
if len(title) > 200:
    flash("Title is too long (max 200 characters)", "error")
    return redirect("/note/new")
```

### Numeric Values

Check a value is **numeric** using `isdigit()`:

```python
value = request.form.get('value', '').strip()

if not value.isdigit():
    flash("Value should be numeric", "error")
    return redirect("/note/new")
```

Check a numeric value is in a **given range** (first converting it to a number)

```python
value = int(value)  # or double(value_str)

if value < 10 or value > 30:
    flash("Value should be between 10 and 30", "error")
    return redirect("/note/new")
```

## Full Example

```python
@app.post("/note")
def add_note():
    # Get form data
    title    = request.form.get('title', '').strip()
    body     = request.form.get('body', '').strip()
    priority = request.form.get('priority', '3').strip()
    tag_list = request.form.getlist('tags')
    pinned   = bool(request.form.get('pinned'))

    # Validate data
    if not title:
        flash("Title is required", "error")
        return redirect("/note/new")

    if len(title) > 40:
        flash("Title is too long (max 40 chars)", "error")
        return redirect("/note/new")

    if not priority.isdigit():
        flash("Priority should be numeric", "error")
        return redirect("/note/new")

    priority = int(priority)
    if priority < 1 or priority > 5:
        flash("Priority should be between 1 and 5", "error")
        return redirect("/note/new")

    # Escape text inputs
    title = html.escape(title)
    body = html.escape(body)

    # Join tags
    tags = ", ".join(tag_list)

    # Add to the database
    with connect_db() as db:
        sql = """
            INSERT INTO note (title, body, priority, tags, pinned)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (title, body, priority, tags, pinned)
        db.execute(sql, params)

        flash(f"Note added")
        return redirect("/")
```

<style>
  #formdemo, #formdemo * {
    box-sizing: border-box;
    font-size: inherit;
  }
  #formdemo {
    width: 22rem;
    margin-inline: auto;
    border: 1px solid currentcolor;
    padding: 0 1rem;
    border-radius: 0.5rem;
    background-color: #3692;
  }
  #formdemo > * {
    display:block;
    margin-block: 1rem;
  }
  #formdemo fieldset label {
    display: inline-block;
    margin-inline: 0.5rem;
  }
  #formdemo input[type="text"],
  #formdemo textarea,
  #formdemo select {
    display: block;
    width: 100%;
  }
</style>



## ⚠️ Important Security Note

✅ Always 'escape' text to avoid **cross-site script (XSS) attacks**. This means that any HTML or JS entered into a text field will not be run when the text is displayed later.

❌ Not doing this allows users to exploit your app by entering script commands into form text fields which your app will then run.

```python
# Escape text to avoid XSS exploits
title = html.escape(title)
body = html.escape(body)
```


