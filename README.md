# Muffin Shop ![](https://img.shields.io/badge/python-3.8-informational) ![](https://img.shields.io/github/license/tassaron/muffin-shop) ![](https://img.shields.io/github/last-commit/tassaron/muffin-shop) [![Follow @brianna on Mastodon](https://img.shields.io/mastodon/follow/1?domain=https%3A%2F%2Ftassaron.com&style=social)](https://tassaron.com/@brianna)

A webapp for small ecommerce sites. Features include: shopping cart, inventory tracking, Stripe integration, basic admin, login system, and emails.

This is a work in progress. The functionality is somewhat modular; see [MODULES.md](MODULES.md) for more information about how modules work.

## Live Instances

-   **[Rainey Arcade](https://rainey.tech)** (shop module used for virtual products)
-   **[Jade Thompson's art portfolio](https://rainey.tech/demo/jlt/)** (gallery module + blog)

## Current Goal

-   Make an instance for _The Rainbow Farm_ (shop module used for real products)

## Long-Term Goal

-   Allow different websites with similar functionality to share a codebase
-   Example: _Website A_ is an online shop with a blue theme and a gallery to showcase images.
-   Example: _Website B_ is an online shop with a red theme and a simple blog.
-   Example: _Website C_ is a simple blog with a white theme and a gallery to showcase images.

## Dependencies

1. Linux
1. Python 3.8+
1. uWSGI
1. Flask
1. [Huey](https://github.com/coleifer/huey) (a task queuer for sending email)
1. SQL-Alchemy
1. WTForms
1. Stripe
1. Webpack
1. ReactJS (for the shop & gallery modules)
1. See [setup.py](setup.py) and [package.json](src/muffin_shop/nodejs/package.json) for more detail

## Setup on Ubuntu Server 20.04

1. Install npm
1. `npm install` in this directory.
1. `npm run build` to bundle/compile static resources with Webpack.
1. Create a Python virtual env, activate it.
   `sudo apt install python3-venv; python3 -m venv env; source env/bin/activate`
1. Do `pip install .` in the root of this repo.
1. Use `python3 scripts/database.py new` to create a new database.
1. Use the `scripts/dev-backend.sh` shell script to run a development uWSGI server (`localhost:5000`).
1. OR use `python3 -m muffin_shop` for Flask's built-in development server.
1. See the [readme inside `/install`](install/README.md) for help with setting up a production server.

## Customizing a New Instance

1. A `.env` file will auto-generate after the first run. It holds secrets, so keep it safe.
1. You can also generate the `.env` file by running `python3 scripts/manage.py init`
1. Set `CONFIG_PATH` to the instance's config directory (copy `config/client/skel` for a template)
1. **Note:** The skeleton config is a mixture of symlinks and copies to maximize my convenience.
1. Example config path: `config/client/<instance_name>`
1. Create `static/client/<instance_name>` and make `css`, `img`, `js` dirs as needed for static assets
1. The `config/client/<instance_name>/modules.json` file defines what modules are loaded and which is the main index.

## Upgrading

1. Stop running server with `systemctl`.
1. Go to the root of this repo.
1. `git pull` the new code.
1. Run `prod-build.sh` to bundle/compile/hocuspocus the JavaScript.
1. Activate the venv and `pip install .`
1. `flask db upgrade` to apply any database migrations.
1. To use the `flask` command you must have `FLASK_APP` in your environment (the `.env` file).

## Development

1. Run `scripts/dev-frontend.sh` to open a split-pane tmux session with live-reloading backend and frontend.
1. Run `scripts/dev-backend.sh` for just a live-reloading backend.
1. Run `python scripts/database.py test --shop` for an example database with products in the shop.
1. Run `scripts/dev-shop.sh` to **replace any existing db** with a shop-testing db, and run `scripts/dev-frontend.sh`

## How it works

1. Systemd starts Nginx and uWSGI
1. Nginx serves files from `/static` directly and passes the other requests through to uWSGI
1. uWSGI creates worker processes each running a Python interpreter. Each worker imports the application callable (Flask object) from `muffin_shop/run.py`.
1. The WSGI application is created by the Main module, specifically by `create_app` defined in `muffin_shop/helpers/main/app_factory.py`
1. When uWSGI receives a connection, it picks one of its idle workers and calls the WSGI application in that process.

## Style

-   Black formatter for Python
-   Prettier formatter for everything else
-   Except HTML because Jinja templates aren't easy to format
-   Unix line endings
-   Absolute Python imports only

## Project Structure

### /static

-   Files that can be cached / files served traditionally by the web server (_e.g._, images, CSS, JavaScript)

### /config

-   Site-specific configuration including logging, modules, html templates, markdown
-   This is only for configuration that can be committed to source control
-   **Note:** Site-specific _secrets_ should be in .env files (_e.g._, `.env.my_site.production`)

### /config/skel

-   "Skeleton" for a new site-specific config - basically a ton of symlinks you can selectively replace

### /src

-   Core pieces of the module system needed by every module
-   Entrypoint: `run.py`

### /src/controllers/`<module>`

-   URL endpoints (routes) which could return a view (template) or JSON

### /src/models/`<module>`

-   Models shape data in the database (using SQLAlchemy)
-   Models manipulate data at the request of controllers

### /src/forms/`<module>`

-   Server-side form validation using WTForms

### /src/helpers/`<module>`

-   Extra helpers for modules such as utility functions, Flask plugins, asynchronous tasks

### /src/react

-   React components to be bundled by Webpack (outputs into `/static/js/dist`)
