import pytest
from marshmallow import Schema, ValidationError

from cronparser.custom_marshmallow_types import CronField
from cronparser.models.cron_values import Range, Single

valid_cases = [
    ("1-2", Range(1, 2)),
    ("1-1", Range(1, )),
    ("1/30", Range(1, 31)),
    ("50/2", Range(50, 52, 54, 56, 58)),
    ("40-50/2", Range(40, 42, 44, 46, 48, 50)),
    ("*/30", Range(0, 30)),
    ("1,2,4,4,6,5", Range(1, 2, 4, 5, 6)),
    ("*", Range(*range(0, 60))),
    ("5", Single(5)),
    ("15", Single(15))
]


class TestSchema(Schema):
    value = CronField(0, 59)


schema = TestSchema()


class TestDOWSchema(Schema):
    value = CronField(0, 6)


DOWschema = TestDOWSchema()


@pytest.mark.parametrize("value,expected", valid_cases)
def test_custom_cron_valid(value, expected):
    payload = dict(value=value)
    actual = schema.load(payload)['value']
    assert actual == expected


dow_valid_cases = [
    ("1-2", Range(1, 2)),
    ("1,2,3", Range(1, 2, 3)),
    ("*", Range(*range(0, 7))),
    ("5", Single(5)),
    ("6/6", Range(6, ))
]


@pytest.mark.parametrize("value,expected", dow_valid_cases)
def test_custom_cron_dow_valid(value, expected):
    payload = dict(value=value)
    actual = DOWschema.load(payload)['value']
    assert actual == expected


invalid_cases = [
    "1-200",
    "1-0",
    "1,2,4,4,6,5,60",
    "*1",
    "*/60",
    "5-10-20",
    "1,2-4,5",
]


@pytest.mark.parametrize("value", invalid_cases)
def test_custom_cron_invalid(value):
    payload = dict(value=value)
    with pytest.raises(ValidationError):
        schema.load(payload)


dow_invalid_cases = [
    "1-7",
    "1,2,7",
    "monday",
    "2/7",
]


@pytest.mark.parametrize("value", dow_invalid_cases)
def test_custom_cron_dow_invalid(value):
    payload = dict(value=value)
    with pytest.raises(ValidationError):
        DOWschema.load(payload)
