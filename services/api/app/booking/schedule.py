from datetime import time


class ProfessionalSchedule:

    WORK_DAYS = {
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
    }

    START_TIME = time(11, 0)
    END_TIME = time(19, 0)