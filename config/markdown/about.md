# {{ site_name }}

This is the about page for {{ site_name }}! It's rendered from a markdown file. Isn't that cool?

## Example

You can combine Markdown and Jinja templating in the same document.

```jinja
{% raw %}
{% for i in range(2) %}
1. This is statement number {{ i+1 }}
{% endfor %}
{% endraw %}
```

### Example Output

{% for i in range(2) %}

1. This is statement number {{ i+1 }}
{% endfor %}
