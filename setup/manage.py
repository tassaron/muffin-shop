#!/usr/bin/env python3
"""
App management script for a Flask application
"""
import argparse
import sys
from tassaron_flask_template import create_env_file
from tassaron_flask_template.main import create_app, init_app
from tassaron_flask_template.main.routes import all_urls


def print_all_urls(stream):
    stream.write("\n".join(all_urls()))


def main():
    """
    Run commandline argument parser
    """
    parser = argparse.ArgumentParser()
    parser.description = "Management script for this Flask application"
    parser.add_argument(
        "action",
        choices=["init", "urls"],
        help=(
            "init: start new project (generate env file)",
            "urls: write all urls to output stream"
        ),
    )
    parser.add_argument(
        "-o",
        help="write to text file instead of stdout",
        metavar="output filename",
        default=None,
    )
    args = parser.parse_args()
    
    if args.action == "urls":
        app = create_app()
        app = init_app(app)
        with app.app_context():
            if args.o is None:
                print_all_urls(sys.stdout)
            else:
                with open(args.o, 'w') as f:
                    print_all_urls(f)

    elif args.action == "init":
        create_env_file()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
