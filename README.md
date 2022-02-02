# Tassaron's Flask Template ![](https://img.shields.io/badge/python-3.8-informational) ![](https://img.shields.io/github/license/tassaron/flask-template) ![](https://img.shields.io/github/last-commit/tassaron/flask-template)  [![Follow @brianna on Mastodon](https://img.shields.io/mastodon/follow/1?domain=https%3A%2F%2Ftassaron.com&style=social)](https://tassaron.com/@brianna)

A work-in-progress template for an advanced Flask webapp with admin, login system and emails built-in, and other common features separated into "modules" defined in `config/modules.json`. A module represents a navigation tab on the website, which can be rearranged and renamed to suit the particular site. Any module can be designated as the homepage. See `MODULES.md` for more information about how these modules are defined.

## Project Goals

1. Allow superficially different websites with shared functionality to share a codebase.
1. Simplify creation of a podcast site, blog, online shop, or any combination of these.
1. Track shop inventory using a SQL database and take purchases using Stripe.
1. Have well-documented setup scripts and clean upgrade paths.

## Setup on Ubuntu Server 20.04

1. Create a virtual env, activate it.
  `sudo apt install python3-venv; python3 -m venv env; source env/bin/activate`
1. Run `pip install -r requirements.txt` to install ALL dependencies including ones for development.
1. Use the `setup.py` file for more minimal dependencies: `pip install .`
1. Use `python3 setup/database.py new` to create a new database.
1. Use the `devserver.sh` shell script to run a development uWSGI server (`localhost:5000`).
1. OR use `python3 -m tassaron_flask` for Flask's built-in development server.
1. See the [readme inside `/setup`](setup/README.md) for help with setting up a production server.

## Customizing

1. A `.env` file will auto-generate after the first run. It holds secrets, so keep it safe.
1. Replace `static/img/logo.png` with your logo. Edit your site name into `.env`
1. The `config/modules.json` file defines what modules are loaded and which is the main index

## Upgrading

1. Stop running server
1. `git pull` the new code
1. Activate the venv and `pip install .`
1. `flask db upgrade` to apply any database migrations
1. To use the `flask` command you must have `FLASK_APP` in your environment

## How it works

1. Systemd starts Nginx and uWSGI
1. Nginx serves files from `tassaron_flask/static` directly and passes the other requests through to uWSGI
1. uWSGI creates worker processes each running a Python interpreter. Each worker imports the application callable (Flask object) from `tassaron_flask/run.py`.
1. The WSGI application is created by the Main module, specifically by `create_app` defined in `tassaron_flask/helpers/main/app_factory.py`
1. When uWSGI receives a connection, it picks one of its idle workers and calls the WSGI application in that process.

## Code Style
* Black formatter
* Absolute imports only
* The `tassaron_flask` package must be installed using pip for the imports to work

## Project Structure
### /tassaron_flask
* Core pieces of the module system needed by every module
* Entrypoint: `run.py`
### /tassaron_flask/static
* Files served traditionally by the web server (*e.g.*, images, CSS)
### /tassaron_flask/templates/`<module>`
* HTML files to be parsed by Jinja templating engine
### /tassaron_flask/controllers/`<module>`
* URL endpoints (routes) which could return a view (template) or JSON
### /tassaron_flask/models/`<module>`
* Models shape data in the database (using SQLAlchemy)
* Models manipulate data at the request of controllers
### /tassaron_flask/forms/`<module>`
* Server-side form validation using WTForms
### /tassaron_flask/helpers/`<module>`
* Extra helpers for modules such as utility functions, Flask plugins, asynchronous tasks