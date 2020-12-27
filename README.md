# Tassaron's Flask Template

A work-in-progress template for an advanced Flask webapp with admin, login system and emails built-in, and other common features separated into "modules" defined in `config/modules.json`. See `MODULES.md` for more information about these modules.

## Project Goals

1. Allow superficially different websites with shared functionality to share a codebase.
1. Simplify creation of a podcast site, blog, online shop, or any combination of these.
1. Track shop inventory using a SQL database and take purchases using Stripe.
1. Have well-documented setup scripts and clean upgrade paths.

## Setup on Ubuntu Server 20.04

1. Create a virtual env, activate it.
  `sudo apt install python3-venv; python3 -m venv env; source env/bin/activate`
1. Install this package: `pip install .`
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
