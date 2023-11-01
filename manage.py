from argparse import ArgumentParser

from integration.app.logging import configure_logging
from cli_commands.common import add_commands
from cli_commands.service import Service


def get_options() -> ArgumentParser:
    parser = ArgumentParser()

    subparsers = parser.add_subparsers()
    subcommands = [Service]
    add_commands(subparsers, subcommands)
    return parser


def main():
    configure_logging()
    parser = get_options()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
