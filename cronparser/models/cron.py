from dataclasses import field

from marshmallow import fields
from marshmallow_dataclass import dataclass

from cronparser.custom_marshmallow_types import CronField
from cronparser.models.cron_values import cron_value_to_string, CronValue


@dataclass
class Cron:
    minute: CronValue = field(metadata={"marshmallow_field": CronField(0, 59)})
    hour: CronValue = field(metadata={"marshmallow_field": CronField(0, 11)})
    dom: CronValue = field(metadata={"marshmallow_field": CronField(0, 31)})
    month: CronValue = field(metadata={"marshmallow_field": CronField(1, 12)})
    dow: CronValue = field(metadata={"marshmallow_field": CronField(0, 6)})
    command: str = fields.String()

    def __repr__(self):
        return f"minute:       {cron_value_to_string(self.minute)}\n" \
               f"hour:         {cron_value_to_string(self.hour)}\n" \
               f"day of month: {cron_value_to_string(self.dom)}\n" \
               f"month:        {cron_value_to_string(self.month)}\n" \
               f"day of week:  {cron_value_to_string(self.dow)}\n" \
               f"command:      {self.command}\n"
