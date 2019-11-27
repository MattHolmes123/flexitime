import datetime

from django.contrib.auth.models import User
from django.utils import timezone

from ..models import FlexiTimeLog


# TODO - Consider making this a setting that is configured at initial setup.
WORKING_DAY = datetime.timedelta(hours=7.5)


class OvertimeService:

    def __init__(self, user: User):
        self.user = user

    def get_current_weeks_overtime(self) -> datetime.timedelta:
        """returns overtime for current week

        :param user: Django request.user
        :return: Overtime this week for supplied user.
        """

        logs = self.get_this_weeks_logs()
        overtime: datetime.timedelta = datetime.timedelta(0)

        for log in logs:
            overtime += _calculate_overtime_for_log(log)

        return overtime

    def get_this_weeks_logs(self):
        """Get this weeks rota records for the supplied user.

        :param user: request user
        :return: Weekly rota records
        """

        today = timezone.now().date()
        diff = 0

        # 1 = Monday, 7 = Sunday
        weekday = today.isoweekday()

        if weekday > 1:
            diff = weekday - 1

        monday = today - datetime.timedelta(days=diff)

        return FlexiTimeLog.objects.filter(
            user=self.user,
            created_at__date__gte=monday,
        )


def _calculate_overtime_for_log(log: FlexiTimeLog) -> datetime.timedelta:
    """Calculates overtime for supplied log record

    :param log: FlexiTimeLog record
    :return: Overtime for the supplied record
    """

    time_in = time_as_td(log.logged_in)
    lunch_break = time_as_td(log.break_duration)
    time_out = time_as_td(log.logged_out)

    if not all([time_in, time_out, lunch_break]):
        return datetime.timedelta(0)

    else:
        return ((time_out - time_in) - lunch_break) - WORKING_DAY


def time_as_td(dt: datetime.time) -> datetime.timedelta:
    """Converts a datetime.time to a datetime.timedelda object.

    :param dt: datetime.time instance.
    :return: datetime.timedelta instance
    """

    return datetime.timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
