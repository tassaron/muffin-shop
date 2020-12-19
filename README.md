# Tassaron's Flask Template
Template for a Flask webapp with login system and emails built-in, and other common features separated into "modules" defined in `modules.json`. See `MODULES.md` for more information about these modules.

## Project Goals
1. Simplify deployment of a new blog, shop, or combined blog + shop.
1. Track inventory using a SQL database and take purchases using Stripe.
1. Have well-documented setup scripts and clean upgrade paths.

## Installation on Ubuntu Server:
1. Create a virtual env, activate it.
  `sudo apt install python3-venv; python3 -m venv env; source env/bin/activate`
1. Install this package: `pip install .`
1. Use `python3 setup/database.py new` to create a new database.
1. Do `python3 -m tassaron_flask_template` for Flask's built-in local development server (`localhost:5000`).
1. OR use the `uwsgi.sh` shell script to run a uWSGI server (which doesn't live-reload).
1. See the [readme inside `/setup`](setup/README.md) for help with setting up a production server.

## Customizing
1. A `.env` file will auto-generate after the first run. It holds secrets, so keep it safe.
1. Replace `static/img/logo.png` with your logo. Edit your site name into `.env`
1. The `modules.json` file defines what optional modules are loaded and which one is the main index

## Upgrading
1. Stop running server
1. `git pull` the new code
1. Activate the venv and `pip install .`
1. `flask db upgrade` to apply any database migrations
