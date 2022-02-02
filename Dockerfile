FROM ubuntu

ENV TZ=Canada/Eastern

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update

RUN apt-get install --no-install-recommends -y \
    build-essential python3-dev python3-venv

WORKDIR /srv/website

COPY /app ./app

COPY /tests ./tests

COPY /setup/website.uwsgi ./uwsgi.ini

COPY /setup/database.py ./database.py

COPY setup.py .

COPY MANIFEST.in .

RUN python3 -m venv /srv/website/env

RUN /srv/website/env/bin/pip3 install .

RUN /srv/website/env/bin/pip3 install pytest pytest-randomly pytest-xdist

RUN /srv/website/env/bin/python3 -m pytest -n 2

RUN /srv/website/env/bin/python3 database.py test

EXPOSE 5000

CMD ["/srv/website/env/bin/uwsgi", "--ini", "/srv/website/uwsgi.ini"]

# Test server without Nginx
# CMD ["/srv/website/env/bin/uwsgi", "--socket", "0.0.0.0:5000", "--protocol=http", "-w", "tassaron_flask.run:app"]
