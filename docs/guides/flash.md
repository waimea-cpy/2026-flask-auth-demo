# Flash Messages

Give feedback to the user after operations / errors.

## Show Messages

```python
flash("Message")
flash("Success message", "success")
flash("Error message", "error")
```
*Note: the message is shown upon next page load*

## Display Messages in a Page

```jinja
{% raw %}{# Show flash messages from any previous events #}
{% include "partials/messages.jinja" %}     {% endraw %}
```
<!-- Ignore the `raw` and `endraw` tags in these Jinja code snippets - they are required for GitHub Pages -->

*Note: you can modify the code for this template partial if needed*

And add suitable CSS to your stylesheet:

```css
/* Flash Status Messages --------------------------------- */

#messages ul {
    width: fit-content;
    margin: 2rem auto;
    padding: 0;
}

#messages .message {
    list-style: none;
    text-align: center;
    margin-bottom: 1rem;
}

#messages .message.success {
    color: var(--pico-color-green-500);
}

#messages .message.error {
    color: var(--pico-color-red-500);
}
```

