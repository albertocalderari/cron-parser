from abc import ABC
from dataclasses import field
from typing import Dict

from marshmallow import pre_load
from marshmallow_dataclass import dataclass

from util import dow_str_to_int


class CronValue(ABC):
    pass


class Single(CronValue):
    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"


class Range(CronValue):
    def __init__(self, *values: int):
        self.values = values

    def __eq__(self, other):
        return self.values == other.values

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.values})"


@dataclass
class Cron:
    minute: CronValue = field()
    hour: CronValue = field()
    dom: CronValue = field()
    month: CronValue = field()
    dow: CronValue = field()
    command: str

    @pre_load
    def _split_fields_and_sanitize_schema(self, data: str, **kwargs) -> Dict[str, str]:
        try:
            minute, hour, dom, month, dow, command = data.split(" ")
            return dict(
                minute=minute,
                hour=hour,
                dom=dom,
                month=month,
                dow=dow_str_to_int(dow),
                command=command
            )
        except ValueError:
            raise BadFormat(f"Cron {data} is not is a valid cron format")

    def __repr__(self):
        return "minute: "


class BadFormat(Exception):
    pass
