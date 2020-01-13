import datetime
from typing import List, Optional, Dict, Iterable

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils import timezone

from ..models import FlexiTimeLog

UserOvertime = Dict[str, Dict[str, datetime.timedelta]]


user_model: User = get_user_model()


class OvertimeService:
    def __init__(self, user: User) -> None:
        self.user: User = user
        self.today: datetime.date = timezone.now().date()

    def get_current_weeks_overtime(self) -> datetime.timedelta:
        """returns overtime for current week

        :return: Overtime this week for supplied user.
        """

        logs = self.get_this_weeks_logs()
        overtime: datetime.timedelta = datetime.timedelta(0)

        for log in logs:
            overtime += calculate_overtime_for_log(log)

        return overtime

    def get_this_weeks_logs(self) -> Iterable[FlexiTimeLog]:
        """Get this weeks rota records for the supplied user.

        :return: Weekly rota records
        """

        monday = self.get_this_mondays_date()

        return FlexiTimeLog.objects.filter(
            user=self.user, log_date__gte=monday,
        ).order_by("log_date")

    def get_this_mondays_date(self) -> datetime.date:
        """Return mondays date for this week.

        :return: Monday's date
        """

        diff = 0
        # 1 = Monday, 7 = Sunday
        weekday = self.today.isoweekday()

        if weekday > 1:
            diff = weekday - 1

        monday = self.today - datetime.timedelta(days=diff)

        return monday

    def get_this_week_as_date_list(self) -> List[datetime.date]:
        """Return this week as a list of dates.

        :return: This week as a list of date objects.
        """

        monday = self.get_this_mondays_date()

        week_list = [monday]

        for day in range(1, 5, 1):
            week_list.append(monday + datetime.timedelta(days=day))

        return week_list

    def can_view_all_user_logs(self) -> bool:
        """Return true if self.user has VIEW_ALL_USER_LOGS permission.

        :return: True if user has specified permission.
        """

        return self.user.has_perm(FlexiTimeLog.VIEW_ALL_USER_LOGS)

    def get_overtime_for_all_users(self) -> UserOvertime:
        """Returns calculated total overtime for each active user."""

        users = user_model.objects.filter(is_active=True)
        user_overtime = {}

        for user in users:
            username: str = user.username
            user_overtime[username] = {
                "overtime": self.get_total_overtime_for_user(user)
            }

        return user_overtime

    def get_total_overtime_for_user(self, user: User) -> datetime.timedelta:
        """Calculated total overtime for the supplied user.

        :param user: User record
        :return: Total overtime for user.
        """

        logs = FlexiTimeLog.objects.filter(user=user)
        overtime: datetime.timedelta = datetime.timedelta(0)

        for log in logs:
            overtime += calculate_overtime_for_log(log)

        return overtime


def calculate_overtime_for_log(log: FlexiTimeLog) -> datetime.timedelta:
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
        return ((time_out - time_in) - lunch_break) - settings.WORKING_DAY


def time_as_td(dt: Optional[datetime.time]) -> datetime.timedelta:
    """Converts a datetime.time to a datetime.timedelta object.

    :param dt: datetime.time instance.
    :return: datetime.timedelta instance
    """

    if dt is None:
        return datetime.timedelta(0)

    return datetime.timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
