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
    name="tassaron's flask template",
    author="tassaron",
    version="20.12.27",  # year.month.day
    packages=[
        "tassaron_flask_template",
        "tassaron_flask_template.main",
        "tassaron_flask_template.about",
        "tassaron_flask_template.shop",
    ],
    package_dir={
        "tassaron_flask_template": "app",
        "tassaron_flask_template.main": "app/main",
        "tassaron_flask_template.about": "app/about",
        "tassaron_flask_template.shop": "app/shop",
    },
    include_package_data=True,
    install_requires=[
        "uWSGI==2.0.19.1",
        "Flask==1.1.2",
        "Flask-Bcrypt==0.7.1",
        "Flask-Login==0.5.0",
        "Flask-Migrate==2.5.3",
        "Flask-MonitoringDashboard==3.1.0",
        "Flask-Reuploaded==0.3.2",
        "Flask-SQLAlchemy==2.4.4",
        "Flask-WTF==0.14.3",
        "email_validator",
        "is_safe_url==1.0",
        "mistune==2.0.0a5",
        "python-dotenv==0.15.0",
        "requests==2.25.1",
        "huey==2.3.0",
    ],
    url="https://github.com/tassaron2/flask-template",
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
