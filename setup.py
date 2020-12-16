from setuptools import setup

setup(
    name="tassaron's flask template",
    version="20.12.13",  # year.month.day
    packages=["tassaron_flask_template", "tassaron_flask_template.blueprints"],
    package_dir={"tassaron_flask_template": "app", "tassaron_flask_template.blueprints": "app/blueprints"},
    include_package_data=True,
    install_requires=[
        "uwsgi",
        "flask",
        "flask-bcrypt",
        "flask-login",
        "flask-sqlalchemy",
        "flask_wtf",
        "flask_reuploaded",
        "flask_migrate",
        "flask_monitoringdashboard",
        "email_validator",
        "is_safe_url",
        "mistune==2.0.0a5",
        "python-dotenv",
        "requests",
    ],
)
