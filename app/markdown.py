from flask import render_template_string, current_app
from mistune import create_markdown


md_to_unsafe_html = create_markdown(escape=False, renderer="html", plugins=["strikethrough"])


def render_markdown(filename):
    try:
        with open(filename, 'r') as f:
            string = f.read()
    except FileNotFoundError:
        if current_app.env == "production":
            current_app.logger.critical("Failed to render missing markdown file: %s", filename)
            return ""
        raise
    string = render_template_string(string)
    # Jinja has now escaped any HTML in the md file
    return md_to_unsafe_html(string)
