from abc import ABC
from dataclasses import field

from marshmallow_dataclass import dataclass


class CronValue(ABC):
    pass


class Always(CronValue):
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
