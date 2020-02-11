import datetime
from typing import Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from main.models import FlexiTimeLog
from main.services.overtime import (
    OvertimeService,
    calculate_overtime_for_log,
    time_as_td,
)


# TODO: Consider moving as_time and as_timedelta to overtime service / utils
def as_time(hour: int, minute: int) -> datetime.time:

    return datetime.time(hour=hour, minute=minute, second=0)


def as_timedelta(hour: int, minute: int) -> datetime.timedelta:

    return datetime.timedelta(hours=hour, minutes=minute, seconds=0)


class OvertimeServiceTestCase(TestCase):

    user_model: settings.AUTH_USER_MODEL

    @classmethod
    def setUpTestData(cls):
        """This is called once before any tests are ran.
        e.g. its like setUp for the class.

        :return:
        """

        cls.user_model = get_user_model()
        cls.user_one = cls.user_model.objects.create_user(
            "User 1", "user@email1.com", "password1", is_active=True
        )
        cls.super_user = cls.user_model.objects.create_superuser(
            "Super User", "superuser@email.com", "SuperUserPassword"
        )

        os = OvertimeService(cls.user_one)
        cls.today = os.today

        test_data = [
            # time_in, break,  time_out
            ((8, 00), (0, 30), (16, 00)),
            ((8, 00), (0, 30), (16, 30)),
            ((8, 00), (0, 30), (16, 00)),
            ((8, 00), (0, 30), (16, 30)),
            ((8, 00), (0, 30), (16, 00)),
        ]

        for i, day in enumerate(os.get_this_week_as_date_list()):
            time_in, lunch, time_out = test_data[i]

            FlexiTimeLog.objects.create(
                user=cls.user_one,
                log_date=day,
                logged_in=as_time(*time_in),
                break_duration=as_time(*lunch),
                logged_out=as_time(*time_out),
            )

    def test_overtime_this_week(self) -> None:

        overtime_service = OvertimeService(self.user_one)

        expected = as_timedelta(1, 0)
        actual = overtime_service.get_current_weeks_overtime()

        self.assertEqual(expected, actual)

    def test_overtime_for_log_zero_overtime(self) -> None:

        log = self._get_log_for_user_one()

        expected = as_timedelta(0, 0)
        actual = calculate_overtime_for_log(log)

        self.assertEqual(expected, actual)

    def test_overtime_for_log_positive_overtime(self) -> None:

        log = self._get_log_for_user_one(logged_in=as_time(7, 0))

        expected = as_timedelta(2, 0)
        actual = calculate_overtime_for_log(log)

        self.assertEqual(expected, actual)

    def test_overtime_for_log_negative_overtime(self) -> None:

        log = self._get_log_for_user_one(
            logged_in=as_time(10, 0), break_duration=as_time(1, 0)
        )

        expected = as_timedelta(-1, -30)
        actual = calculate_overtime_for_log(log)

        self.assertEqual(expected, actual)

    def test_bug_with_time_as_td(self):
        # time_as_td needs to work with None
        # fixes this: AttributeError: 'NoneType' object has no attribute 'hour'

        logged_out = None

        expected = as_timedelta(0, 0)
        actual = time_as_td(logged_out)

        self.assertEqual(expected, actual)

    def test_overtime_for_log_with_incomplete_entry(self):
        log = self._get_log_for_user_one(logged_out=None)

        expected = as_timedelta(0, 0)
        actual = calculate_overtime_for_log(log)

        self.assertEqual(expected, actual)

    def _get_log_for_user_one(
        self,
        *,
        logged_in: Optional[datetime.time] = as_time(9, 00),
        break_duration: Optional[datetime.time] = as_time(0, 30),
        logged_out: Optional[datetime.time] = as_time(17, 00)
    ) -> FlexiTimeLog:
        """Returns a FlexiTimeLog object defaulting to 0 hour overtime day.

        :param logged_in: Time logged in
        :param break_duration: Total break duration
        :param logged_out: Time logged out
        :return: FlexiTimeLog object
        """

        extra = {}

        for field, val in (
            ("logged_in", logged_in),
            ("break_duration", break_duration),
            ("logged_out", logged_out),
        ):
            if val is not None:
                extra[field] = val

        return FlexiTimeLog.objects.create(
            user=self.user_one, log_date=self.today, **extra
        )

    def test_super_user_can_see_all_user_overtime(self):

        overtime_service = OvertimeService(self.super_user)

        expected = True
        actual = overtime_service.can_view_all_user_logs()

        self.assertEqual(expected, actual)

    def test_user_one_cannot_see_all_user_overtime(self):
        overtime_service = OvertimeService(self.user_one)

        expected = False
        actual = overtime_service.can_view_all_user_logs()

        self.assertEqual(expected, actual)

    # TODO rename
    def test_all_logs(self):
        overtime_service = OvertimeService(self.super_user)

        expected = {
            "User 1": {"overtime": as_timedelta(1, 0)},
            "Super User": {"overtime": datetime.timedelta(0)},
        }
        actual = overtime_service.get_overtime_for_all_users()

        self.assertEqual(expected, actual)
