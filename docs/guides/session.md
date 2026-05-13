# Session Management

## Uses of the Session

The session is used for storing data that lasts between HTTP requests (in other words, between page loads / refreshes).

The session is useful for storing:
- Login state (true/false, username, etc.)
- Order carts
- etc.


## Using the Session

### Set a value:

```python
session['key'] = value
```

### Get a value:

```python
value = session.get('key')
```

#### With a default if not present:

```python
value = session.get('key', 'default')
```

### Delete a value:

```python
session.pop('key', None)
```

### Clear all values

```python
session.clear()
```

