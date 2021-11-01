from datetime import datetime
from enum import Enum
import copy
from functools import wraps
from dateutil.relativedelta import *

__all__ = ['t', 'TimePeriod', 'TimeScale', 'RailsTime']

class TimePeriod(Enum):
    DAY = 'days'
    WEEK = 'weeks'
    MONTH = 'months'
    YEAR = 'years'

class TimeScale(Enum):
    FUTURE = 'future'
    PAST = 'past'

class RailsTime(object):

    class WeekDays(Enum):
        MONDAY = MO

    def __init__(self, integer:int, timezone:str = None) -> None:

        if type(integer) != int:
            raise TypeError("Specify an Int")
        
        if integer < 0:
            raise ValueError("Specify positive integer")

        self.reference_integer : int = integer
        self.start_day_enum = MO(2)

        self.use_format = '%c'
        self.final_datetime : datetime = None
        self.time_scale : TimeScale = None
        self.time_period : TimePeriod = None
        self.anchor_datetime : datetime = datetime.now()

    @property
    def years(self):
        self.time_period = TimePeriod.YEAR
        return self

    @property
    def months(self):
        self.time_period = TimePeriod.MONTH
        return self

    @property
    def weeks(self):
        self.time_period = TimePeriod.WEEK
        return self

    @property
    def days(self):
        self.time_period = TimePeriod.DAY
        return self

    def _perform(self):
        # iterate over all the methods
        instance = copy.copy(self)

        rd_kwargs = {
            'weekday': instance.start_day_enum,
            instance.time_period.value : instance.reference_integer
        }

        rd = relativedelta(**rd_kwargs)

        if instance.time_scale.value == 'future':
            self.final_datetime = instance.anchor_datetime + rd
        
        if instance.time_scale.value == 'past':
            self.final_datetime = instance.anchor_datetime - rd

    @property
    def ago(self):
        self.time_scale = TimeScale.PAST
        return self

    @property
    def from_now(self):
        self.time_scale = TimeScale.FUTURE
        return self

    def week_start(self, day):
        self.week_start_day = MO
        return self

    def _from(self, anchor_datetime : datetime):
        self.time_scale = TimeScale.FUTURE
        self.anchor_datetime = anchor_datetime
        return self

    def to_d(self, use_format='%c'):
        self.use_format = use_format
        self._perform()
        return self

    def __str__(self) -> str:
        if self.final_datetime is None:
            raise ValueError("Need to call .to_d()")
        return self.final_datetime.strftime(self.use_format)

    def __repr__(self) -> str:
        return str(self)

t = lambda x, **kwargs : RailsTime(x, **kwargs)

print(t(2).days._from(anchor_datetime=datetime(day=1, month=10, year=2021)).to_d())
print(t(3).days.ago.to_d())
print(t(4).days.from_now.to_d())
print(t(3).days.ago.to_d())

