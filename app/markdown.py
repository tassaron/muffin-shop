from mistune import create_markdown


# Don't let Mistune escape HTML because Jinja does it later
md_to_html = create_markdown(escape=False, renderer="html", plugins=["strikethrough"])
