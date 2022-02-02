from setuptools import setup
from os import path


try:
    with open(
        path.join(path.abspath(path.dirname(__file__)), "README.md"), encoding="utf-8"
    ) as f:
        long_description = f.read()
except Exception:
    long_description = "missing README.md"


setup(
    name="tassaron flask",
    author="tassaron",
    version="0.0.0",
    include_package_data=True,
    install_requires=[
        "uWSGI",
        "Flask",
        "Bcrypt-Flask",
        "Flask-Login",
        "Flask-Migrate",
        "Flask-MonitoringDashboard",
        "Flask-Reuploaded",
        "Flask-SQLAlchemy",
        "Flask-WTF",
        "email_validator",
        "is_safe_url",
        "mistune",
        "python-dotenv",
        "requests",
        "huey",
    ],
    url="https://github.com/tassaron/flask-template",
    license="MIT",
    description="my template for an advanced Flask app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="flask uwsgi modular template",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Framework :: Flask",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
)
