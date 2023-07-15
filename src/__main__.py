"""
Entrypoint for `python -m modulename` starts a Flask development server
"""
from muffin_shop.run import application

application.run(debug=True)
