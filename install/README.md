# Installation instructions

## Set up Ubuntu

1. Make sudoer account if needed.
1. **Stay authenticated as root** from sudoer account: `sudo -s`
1. Lock root account: `passwd -l root`
1. Edit SSH config: `nano /etc/ssh/sshd_config`
    1. Disable RootLogin and change SSH port if desired.
    1. Setup an SSH key and disable PasswordAuthentication.
1. Install Nginx: `apt install -y nginx`
1. Configure firewall: `ufw allow [YOUR-SSH-PORT]; ufw allow 'Nginx Full'`
1. Start firewall: `ufw enable`
1. Install dependencies needed to compile uWSGI later: `apt install build-essential gcc python3-dev`
1. Make user account for the app: `adduser --system --home /srv/website website`

## Install app

1. **Switch to `website` user** and directory: `sudo -su website && cd ~website`
1. Clone repo from GitHub: `git clone https://github.com/tassaron/muffin-shop`
1. Install [nvm](https://github.com/nvm-sh/nvm#installing-and-updating)
1. Install latest NodeJS: `nvm install node`
1. Run `npm install` to create a gigantic `node_modules` directory because ya _gotta_ have a gigantic `node_modules` directory
1. Run `npm run build` to compile the React components into `static/js/dist/bundle.js`
1. Make Python virtual environment: `python3 -m venv env`
1. Activate virtual environment: `source env/bin/activate`
1. Install using Pip: `pip install .`

## Configure app

1. **Be the `website` user with venv active**
1. Copy template for `.env` file: `cp .env.example .env`
1. Edit `.env` to set `SITE_NAME`
1. Each instance has a `config` and `static` tree which is decided by `CONFIG_PATH` in `.env`
1. Example: `CONFIG_PATH=config/client/<instance_name>`
1. Create instance directories by copying `config/client/skel` to the aforementioned config dir
1. Create `static/client/<instance_name>` for static assets
1. Customize `config/client/<instance_name>/modules.json`, `config/client/<instance_name>/markdown/about.md`, etc. as needed
1. Set any other variables in `.env` as needed for the modules enabled
    - For example, you need to set `STRIPE_` variables to take payments for a shop module
    - The security of your `.env` file is very important. It should not be readable by anonymous Unix users nor be committed to source control
1. Customize HTML inside `config/client/<instance_name>/templates` as needed.

## Run tests

1. **Be the `website` user with venv active**
1. Install pytest with `pip install pytest`.
1. Run tests without hitting APIs: `pytest -k 'not payment and not email'`
    - If your `EMAIL_API_KEY` is undefined/empty, it is safe to run the email tests (emails will be printed in the log instead of being sent)
    - If you have a testing API key or `STRIPE_API_KEY` is undefined/empty, then payment tests can be included.
    - **Do not run payment tests with a production API key.**

## Create database

1. **Be the `website` user with venv active**
1. Initialize app with `python3 scripts/manage.py init` (optional; this creates a secret key but the app also creates one if it's missing)
1. Make database: `python3 scripts/database.py new`. Copy the admin user's password (change it later using the website)

## Create services

1. **Be the sudo user again** (exit from website user if following chronologically)
1. Edit your domain name into this file: `nano install/website.nginx`
1. Edit `install/website.service` and `install/huey.service` if the website directory is not `/srv/website/`
1. Set permissions: `chown -R website:nogroup /srv/website; chmod -R 644 /srv/website`
1. Place Nginx config: `cp install/website.nginx /etc/nginx/sites-available/<instance_name>.nginx`
    - Standard practice is to name Nginx config files after the domain name, so you may want to do that instead
1. Enable Nginx config: `ln -s /etc/nginx/sites-available/website.nginx /etc/nginx/sites-enabled/website.nginx`
1. Delete default Nginx config: `rm /etc/nginx/sites-enabled/default`
1. Place Systemd units: `cp install/*.service /etc/systemd/system`
1. Start uWSGI service: `systemctl start website.service`
1. Start Huey consumer service: `systemctl start huey.service`
1. Restart Nginx: `systemctl restart nginx`
1. Enable the services to start at boot: `systemctl enable website.service huey.service`

## Enabling HTTPS

1. Use [Certbot](https://certbot.eff.org/) to get an SSL cert that renews automatically, which also has a handy option to convert the Nginx config for you.
1. If you get a 500 error, double-check that `/srv/website/website.sock` is owned by the `www-data` group
