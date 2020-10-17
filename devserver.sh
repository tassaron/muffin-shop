# Use this to test a uWSGI server without Nginx in front
# Flask's built-in dev server works too, but this gets us closer to a production environment
uwsgi --socket 0.0.0.0:5000 --protocol=http -w rainbow_shop.__init__:app
