import json
from argparse import ArgumentParser
from typing import Sequence, Union, Type, IO, TypeAlias

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class BaseCommand:
    name: str

    @classmethod
    def add_args(cls, parser: ArgumentParser):
        pass

    @classmethod
    def add_subcommands(cls, parser: ArgumentParser):
        subcmds = cls.subcommands()
        if not subcmds:
            return
        subparsers = parser.add_subparsers()
        add_commands(subparsers, subcmds)

    @classmethod
    def subcommands(cls):
        return []


class RunnableCommand(BaseCommand):
    @classmethod
    def run(cls, args):
        raise NotImplementedError()

    @staticmethod
    def _write_data(data: Union[BaseModel, list[BaseModel]], output: IO):
        data = jsonable_encoder(data)
        data = json.dumps(data, indent=4, ensure_ascii=False)
        output.write(data)


def add_commands(subparsers, commands: Sequence[Union[Type[RunnableCommand], Type[BaseCommand]]]):
    for cmd in commands:
        cmd_parser = subparsers.add_parser(cmd.name)
        cmd.add_args(cmd_parser)
        cmd.add_subcommands(cmd_parser)
        if issubclass(cmd, RunnableCommand):
            cmd_parser.set_defaults(func=cmd.run)
