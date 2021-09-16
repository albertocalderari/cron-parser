import argparse

from marshmallow.exceptions import ValidationError

from cronparser.models.cron import Cron
from cronparser.models.exceptions import InvalidCron
from cronparser.util import cron_to_dict


def main():
    parser = argparse.ArgumentParser("cronparser", description="A CLI to parse a cron command")
    parser.add_argument("cron_expr", help='The cron expression in quotes i.e. */30 0 1,15 * 1-3')
    args = parser.parse_args()
    error = ""
    try:
        cron = app(args.cron_expr)
        print(cron)
    except ValidationError as e:
        error += "Errors:\n"
        for k, v in e.messages.items():
            error += f"Location: {k} Errors: {','.join(v)}\n"
    if error:
        raise InvalidCron(error)


def app(cron: str) -> Cron:
    cron_dict = cron_to_dict(cron)
    return Cron.Schema().load(cron_dict)
