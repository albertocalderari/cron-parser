import argparse

from marshmallow.exceptions import ValidationError

from models.cron import Cron
from models.exceptions import InvalidCron
from util import cron_to_dict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cron_expr")
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
