# Jinja Template Guide

<!-- Ignore the `raw` and `endraw` tags in these Jinja code snippets - they are required for GitHub Pages -->

## Templates

### Variables

```jinja
{% raw %}{# Variables use {{...}} syntax... #}

{{ variable }}
{{ dict.key }}
{{ list[0] }}       {% endraw %}
```

### Conditionals

```jinja
{% raw %}{# Conditional statements let you make choices... #}

{# Conditional values #}
{{ 'this' if condition }}
{{ '★' if note.important }}
{# ... and with alternative values #}
{{ 'this' if condition else 'that' }}
{{ session['username'] if session['logged_in'] else 'Guest' }}

{# Simple if #}
{% if condition %}
    ...
{% endif %}

{# With other options #}
{% if condition %}
    ...
{% elif other %}
    ...
{% else %}
    ...
{% endif %}      {% endraw %}
```

```jinja
{% raw %}{# Conditional operators... #}

{% if age >= 18 %}
{% if name == "John" %}
{% if count != 0 %}
{% if score > 50 and score < 100 %}
{% if is_admin or is_moderator %}      {% endraw %}
```

```jinja
{% raw %}{# Using conditions to check variable values... #}

{# Check if value exists and is not empty #}
{% if variable %}
{% if not variable %}

{# Check for None/null #}
{% if user is none %}
{% if user is not none %}

{# Check if value is in a list #}
{% if item in items %}
{% if 'admin' in user.roles %}      {% endraw %}
```

### Loops

```jinja
{% raw %}{# Looping through values and lists... #}

{# Loop from 1 to 10 #}
{% for i in range(1, 11) %}
    {{ i }}
{% endfor %}

{# Simple loop through a list #}
{% for item in items %}
    {{ item }}
{% endfor %}

{# Loop With 'else' option if list is empty #}
{% for item in items %}
    {{ item }}
{% else %}
    No items!
{% endfor %}        {% endraw %}
```

```jinja
{% raw %}{# Accessing loop variables... #}

{# Accessing the loop counter #}
{% for item in items %}
    Item {{ loop.index }}: {{ item }}
{% endfor %}

{# Other loop variables #}
{% for item in items %}
    {{ loop.first }}    {# True if first iteration #}
    {{ loop.last }}     {# True if last iteration #}
    {{ loop.length }}   {# Total number of items #}
{% endfor %}        {% endraw %}
```

### Include Partials

```jinja
{% raw %}{# If you need to include another, partial template... #}

{% include "partials/header.jinja" %}       {% endraw %}
```

## Template Filters

### Date/Time Filters
```jinja
{% raw %}{# These filters modify a data/time... #}

{{ note.created | local | format }}        {# Local timezone, nice format #}
{{ note.created | format_date }}           {# Show nice date only #}
{{ note.created | format_time }}           {# Show nice time only #}
{{ note.created | format_human }}          {# "2 hours ago" style format #}
{{ note.created | format("YYYY-MM-DD") }}  {# Custom format #}
{{ now() | format }}                       {# Current time #}{% endraw %}
```

### Text Filters
```jinja
{% raw %}{# These filter modify text... #}

{# Text conversion #}
{{ text | upper }}    {# to UPPER CASE #}
{{ text | lower }}    {# to lower case #}
{{ text | title }}    {# to Title Case #}

{# Shorten long text #}
{{ long_text | truncate(100) }}

{# Convert \n to <br> tags and \n\n to <p> tags #}
{{ note.body | paragraphs }}        {% endraw %}
```

