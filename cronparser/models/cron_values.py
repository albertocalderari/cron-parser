from abc import ABC


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


def cron_value_to_string(value: CronValue) -> str:
    if isinstance(value, Single):
        return f"{value.value}"
    elif isinstance(value, Range):
        return " ".join([str(v) for v in value.values])
    else:
        raise NotImplementedError(f"Value {type(value)} not supported")
