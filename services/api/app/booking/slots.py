from datetime import datetime, timedelta
from typing import List

from app.booking.schedule import ProfessionalSchedule


def generate_daily_slots(service_duration_minutes: int):

    slots = []

    current = datetime.combine(
        datetime.today(),
        ProfessionalSchedule.START_TIME
    )

    end = datetime.combine(
        datetime.today(),
        ProfessionalSchedule.END_TIME
    )

    duration = timedelta(minutes=service_duration_minutes)

    while current + duration <= end:
        slots.append(current.time())
        current += duration

    return slots