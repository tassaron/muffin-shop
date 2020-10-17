# The Rainbow Farm
This is an online store made for The Rainbow Farm's website (which is not yet online). Made using Python and the Flask framework.


## Installation on Ubuntu Server:
1. Create a virtual env, activate it.
  `sudo apt install python3-venv; python3 -m venv env; source env/bin/activate`
1. Install this package: `pip install .`
1. Use the `database.py` script in `/bin` to create a new database.
1. Do `python3 -m rainbow_shop` for Flask's built-in local development server (`localhost:5000`).
1. Use the `devserver.sh` shell script to run a uWSGI server (`0.0.0.0:5000`).
1. See the [readme inside `/setup`](setup/README.md) for help with setting up a production server.
