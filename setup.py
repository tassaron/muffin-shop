from setuptools import setup

setup(
    name="the rainbow shop",
    version="20.10.22",  # year.month.day
    packages=["rainbow_shop", "rainbow_shop.blueprints"],
    package_dir={"rainbow_shop": "app", "rainbow_shop.blueprints": "app/blueprints"},
    include_package_data=True,
    install_requires=[
        "uwsgi",
        "flask",
        "flask-bcrypt",
        "flask-login",
        "flask-sqlalchemy",
        "flask_wtf",
        "flask_migrate",
        "flask_monitoringdashboard",
        "email_validator",
        "is_safe_url",
        "mistune==2.0.0a5",
        "python-dotenv",
    ],
)
