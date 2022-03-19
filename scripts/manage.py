#!/usr/bin/env python3
"""
App management script for a Flask application
"""
import argparse
import sys
from muffin_shop.flask import create_env_file
from muffin_shop.helpers.main.app_factory import create_app, init_app
from muffin_shop.helpers.main.util import all_urls


def print_all_urls(stream):
    stream.write("\n".join(all_urls()) + "\n")


def main():
    """
    Run commandline argument parser
    """
    parser = argparse.ArgumentParser()
    parser.description = "Management script for this Flask application"
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("action", help="init: start new project (generate env file)", nargs="?", metavar="init")
    actions.add_argument("urls", help="urls: write all urls to stdout", nargs="?")

    parser.add_argument(
        "-o",
        help="redirect stdout to text file",
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
