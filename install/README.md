# First setup
1. Switch to root from sudoer account: `sudo -s`
1. Lock root account: `passwd -l root`
1. Edit SSH config: `nano /etc/ssh/sshd_config`
  1. Change SSH port and disable RootLogin.
  1. Setup an SSH key and disable PasswordAuthentication.
1. Install Nginx: `apt install -y nginx`
1. Configure firewall: `ufw allow [YOUR-SSH-PORT]; ufw allow 'Nginx Full'`
1. Start firewall: `ufw enable`
1. Make user account for the app: `adduser --system --home /srv/website website`
1. Clone repo from GitHub: `git clone https://github.com/tassaron/muffin-shop /srv/website`
1. Make Python virtual environment: `cd ~website; python3 -m venv env`
1. Activate virtual environment: `source env/bin/activate`
1. Install dependencies needed to compile uWSGI: `apt install build-essential gcc python3-dev`
1. Install using Pip: `pip install .`
1. Edit your domain name into this file: `nano install/website.nginx`
  1. Standard practice is to name Nginx config files after the domain name, but it's not necessary
1. Place Nginx config: `cp install/website.nginx /etc/nginx/sites-available/website.nginx`
1. Enable Nginx config: `ln -s /etc/nginx/sites-available/website.nginx /etc/nginx/sites-enabled/website.nginx`
1. Place Systemd units: `cp install/*.service /etc/systemd/system`
1. Copy template for `.env` file: `cp .env.example .env`
1. Edit `.env` to set `SITE_NAME` and change the value of `FLASK_ENV` to `production`
1. Customize `config/modules.json`, `config/markdown/about.md`, and `static/img/logo.png` as needed
1. Set any other variables in `.env` as needed for the modules enabled
  1. For example, you need to set `STRIPE_` variables to take payments for a shop module
  1. The security of your `.env` file is very important. It should not be readable by anonymous Unix users nor be committed to source control
1. Customize HTML inside `config/templates` as needed.
1. Set permissions: `chown -R website:www-data /srv/website; chmod -R 755 /srv/website`
1. Make database: `sudo -u website python3 /srv/website/scripts/database.py new`
1. Start uWSGI service: `systemctl start website.service`
1. Restart Nginx: `systemctl restart nginx`
1. Exit from root account: `exit`
1. At this point you can use [Certbot](https://certbot.eff.org/) to get an SSL cert that renews automatically, which also has a handy option to convert the Nginx config for you.
