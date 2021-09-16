import re

import typing
from marshmallow import ValidationError, fields

from cronparser.models.cron_values import Range, Single


class CronField(fields.Field):
    def __init__(self, min_range: int, max_range: int, wildcard="*", *args, **kwargs):
        super(CronField, self).__init__(*args, **kwargs)
        self.max_range = max_range
        self.min_range = min_range
        self.wildcard = wildcard

        self._single_rgx = r'^[0-9]+$'
        self._range_rgx = r'^[0-9]+-[0-9]+$'
        self._stepped_range_rgx = rf'^([0-9]+|\{self.wildcard})/[0-9]+$'
        self._list_rgx = r'^[0-9]+(?:,[0-9]+)*$'

    def _repr_args(self) -> str:
        return f"{self.__class__.__name__}(min={self.min_range}, max={self.max_range}, wildcard={self.wildcard})"

    def deserialize(
            self,
            value: str,
            attr: typing.Optional[str] = None,
            data: typing.Optional[typing.Mapping[str, typing.Any]] = None,
            **kwargs
    ):
        if value == self.wildcard:
            return Range(*range(self.min_range, self.max_range+1))
        elif '-' in value:
            return self._deserialize_range(value)
        elif '/' in value:
            return self._deserialize_stepped_range(value)
        elif ',' in value:
            return self._deserialize_list(value)
        else:
            return self._deserialize_single(value)

    def _deserialize_range(self, value: str):
        rgx = self._range_rgx
        if re.fullmatch(rgx, value):
            lower, upper = value.split("-")
            int_lower, int_upper = int(lower), int(upper)
            if int_lower > int_upper:
                raise ValidationError(f"Lower bound value {lower} needs to be smaller than upper bound value {upper}")
            elif int_upper > self.max_range or int_lower < self.min_range:
                raise ValidationError(f"Range {lower}-{upper} must be within {self.min_range}-{self.max_range}")
            rng = range(int_lower, int_upper + 1)
            return Range(*rng)
        else:
            raise ValidationError(f"Range value {value} des not match [v1-v2] "
                                  f"where v1 <= v2 and values are within {self.min_range} and {self.max_range}")

    def _deserialize_stepped_range(self, value: str):
        rgx = self._stepped_range_rgx
        if re.fullmatch(rgx, value):
            value = value.replace(self.wildcard, "0")
            lower, step = value.split("/")
            int_lower, int_step = int(lower), int(step)
            if int_step > self.max_range:
                raise ValidationError(f"Step needs to be smaller than {self.max_range}")
            rng = range(int_lower, self.max_range + 1, int_step)
            return Range(*rng)
        else:
            raise ValidationError(f"Range value {value} des not match [v1/v2] where"
                                  f" v1 <= v2 and values are within {self.min_range} and {self.max_range}")

    def _deserialize_list(self, value: str):
        rgx = self._list_rgx
        if re.fullmatch(rgx, value):
            values = value.split(",")
            int_values = set([int(v) for v in values])
            if max(int_values) > self.max_range or min(int_values) < self.min_range:
                raise ValidationError(f"Range must be within {self.min_range} and {self.max_range}")
            return Range(*int_values)
        else:
            raise ValidationError(f"Range value {value} des not match [v1-v2] "
                                  f"where v1 < v2 and values are within {self.min_range} and {self.max_range}")

    def _deserialize_single(self, value: str):
        rgx = self._single_rgx
        if re.fullmatch(rgx, value):
            int_value = int(value)
            if int_value > self.max_range or int_value < self.min_range:
                raise ValidationError(f"Value must be within {self.min_range} and {self.max_range}")
            return Single(int_value)
        else:
            raise ValidationError(f"Range value {value} des not match [v1-v2] "
                                  f"where v1 < v2 and values are within {self.min_range} and {self.max_range}")