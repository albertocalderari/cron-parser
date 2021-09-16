import pytest
from marshmallow import ValidationError

from cronparser.main import app
from cronparser.models.cron import Cron
from cronparser.models.cron_values import Range, Single


def test_success():
    expected = Cron(
        minute=Range(0, 15, 30, 45),
        hour=Single(0),
        dom=Range(1, 15),
        month=Range(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
        dow=Range(1, 2, 3, 4, 5),
        command="/usr/bin/find"
    )

    expected_str = "minute:       0 15 30 45\n" \
                   "hour:         0\n" \
                   "day of month: 1 15\n" \
                   "month:        1 2 3 4 5 6 7 8 9 10 11 12\n" \
                   "day of week:  1 2 3 4 5\n" \
                   "command:      /usr/bin/find\n"

    cron_str = "*/15 0 1,15 * 1-5 /usr/bin/find"
    actual = app(cron_str)

    assert expected == actual, "Cron object not matching expected"
    assert expected_str == str(actual), "Sringified cron not matching expected"


def test_failure():
    cron_str = "*/60 0 1,15 * 1-6 /usr/bin/find"
    with pytest.raises(ValidationError) as e:
        app(cron_str)
        assert {'minute': ['Step needs to be smaller than 59']} == e.messages
