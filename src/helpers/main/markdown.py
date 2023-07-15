from flask import render_template_string, current_app
from mistune import create_markdown
import os


md_to_unsafe_html = create_markdown(
    escape=False, renderer="html", plugins=["strikethrough"]
)


def render_markdown(filename):
    path = f"{current_app.config['CONFIG_PATH']}/markdown/{filename}"
    if not os.path.exists(path):
        current_app.logger.error("Failed to render markdown at %s", path)
        return ""
    try:
        with open(path, "r") as f:
            string = f.read()
    except:
        if not current_app.debug:
            current_app.logger.critical(
                "Failed to render missing markdown file: %s", filename, exc_info=True
            )
            return ""
        raise
    string = render_template_string(string)
    # Jinja has now escaped any HTML in the md file
    return md_to_unsafe_html(string)
