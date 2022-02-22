from setuptools import setup, find_packages
from os import path
import re


try:
    with open(
        path.join(path.abspath(path.dirname(__file__)), "README.md"), encoding="utf-8"
    ) as f:
        long_description = f.read()
except Exception:
    long_description = "missing README.md"


PACKAGE_NAME = 'muffin_shop'
SOURCE_DIRECTORY = 'src'
SOURCE_PACKAGE_REGEX = re.compile(rf'^{SOURCE_DIRECTORY}')

source_packages = find_packages(include=[SOURCE_DIRECTORY, f'{SOURCE_DIRECTORY}.*'])
proj_packages = [SOURCE_PACKAGE_REGEX.sub(PACKAGE_NAME, name) for name in source_packages]


setup(
    name=PACKAGE_NAME,
    author="tassaron",
    version="0.0.0",
    packages=proj_packages,
    package_dir={PACKAGE_NAME: SOURCE_DIRECTORY},
    include_package_data=True,
    install_requires=[
        "uWSGI",
        "Flask",
        "Bcrypt-Flask",
        "Flask-Login",
        "Flask-Limiter",
        "Flask-Migrate",
        "Flask-MonitoringDashboard",
        "Flask-Reuploaded",
        "Flask-SQLAlchemy",
        "Flask-WTF",
        "PyJWT",
        "email_validator",
        "is_safe_url",
        "mistune",
        "python-dotenv",
        "requests",
        "huey",
        "stripe",
    ],
    url="https://github.com/tassaron/muffin-shop",
    license="MIT",
    description="a Flask app for small ecommerce sites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="flask uwsgi modular template shop",
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
