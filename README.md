# Tassaron's Flask Template
This git repo started as another project for a specific website, but I've forked it off at this point to serve as a template for future webapps. It has a login system and the groundwork for a more complex webapp (blueprints, tests, monitoring, setup scripts, migrations).


## Installation on Ubuntu Server:
1. Create a virtual env, activate it.
  `sudo apt install python3-venv; python3 -m venv env; source env/bin/activate`
1. Install this package: `pip install .`
1. Use the `database.py` script in `/setup` to create a new database.
1. Do `python3 -m tassaron_flask_template` for Flask's built-in local development server (`localhost:5000`).
1. Use the `uwsgi.sh` shell script to run a uWSGI server (`0.0.0.0:5000`).
1. See the [readme inside `/setup`](setup/README.md) for help with setting up a production server.


## Upgrading
1. Stop running server
1. `git pull` the new code
1. Activate the venv and `pip install .`
1. `flask db upgrade` to apply any database migrations
