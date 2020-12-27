# Tassaron's Flask Template

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
1. OR use `python3 -m tassaron_flask_template` for Flask's built-in development server.
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
1. Nginx serves files from `app/static` directly and passes the other requests through to uWSGI
1. uWSGI creates worker processes each running a Python interpreter. Each worker imports the application callable (Flask object) from `app/run.py`.
1. When uWSGI receives a connection, it picks one of its idle workers and calls the WSGI application in that process.
1. The Main module `app/main` contains the `create_app` function and core systems like login, email, and admin
1. The Main module's `init_app` function is called next to import other modules
