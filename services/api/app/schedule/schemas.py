from datetime import date, time
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class WeeklyScheduleRule(BaseModel):
    """
    day_of_week sigue la convención de Python:
    0 = Monday
    1 = Tuesday
    2 = Wednesday
    3 = Thursday
    4 = Friday
    5 = Saturday
    6 = Sunday
    """

    day_of_week: int = Field(..., ge=0, le=6)
    is_working_day: bool
    start_time: Optional[time] = None
    end_time: Optional[time] = None

    @model_validator(mode="after")
    def validate_working_day_window(self):
        if self.is_working_day:
            if self.start_time is None or self.end_time is None:
                raise ValueError(
                    "Working days must include start_time and end_time"
                )

            if self.end_time <= self.start_time:
                raise ValueError(
                    "end_time must be greater than start_time"
                )
        else:
            if self.start_time is not None or self.end_time is not None:
                raise ValueError(
                    "Non-working days must not define start_time or end_time"
                )

        return self


class DailyBreak(BaseModel):
    day_of_week: int = Field(..., ge=0, le=6)
    start_time: time
    end_time: time
    label: str = Field(..., min_length=1, max_length=120)

    @model_validator(mode="after")
    def validate_break_window(self):
        if self.end_time <= self.start_time:
            raise ValueError(
                "Break end_time must be greater than start_time"
            )
        return self


class ScheduleTemplateUpdate(BaseModel):
    weekly_rules: List[WeeklyScheduleRule]
    breaks: List[DailyBreak]


class ScheduleTemplateResponse(BaseModel):
    weekly_rules: List[WeeklyScheduleRule]
    breaks: List[DailyBreak]


class DateBlockCreate(BaseModel):
    block_date: date
    start_time: time
    end_time: time
    reason: str = Field(..., min_length=1, max_length=200)

    @model_validator(mode="after")
    def validate_block_window(self):
        if self.end_time <= self.start_time:
            raise ValueError(
                "Block end_time must be greater than start_time"
            )
        return self


class DateBlockResponse(BaseModel):
    id: UUID
    block_date: date
    start_time: time
    end_time: time
    reason: str


class DayScheduleResponse(BaseModel):
    target_date: date
    day_of_week: int
    is_working_day: bool
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    breaks: List[DailyBreak]
    date_blocks: List[DateBlockResponse]


class DeleteDateBlockResponse(BaseModel):
    deleted: bool
    block_id: UUID