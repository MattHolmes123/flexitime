import datetime

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


def time_now() -> datetime.time:
    """Function that returns a rounded login time.
    Rounds in 5 minute increments.

    :return: time now
    """

    now = timezone.now()
    minutes = now.minute

    remainder = minutes % 5

    if remainder > 0:
        add_on = datetime.timedelta(minutes=(5 - remainder))
    else:
        add_on = datetime.timedelta(0)

    return (now + add_on).time()


# TODO: Decide best way to do this (Do we need a constants.py file or anything).
_perm_view_all_user_logs = "view_all_user_logs"


class FlexiTimeLog(models.Model):
    VIEW_ALL_USER_LOGS = f"main.{_perm_view_all_user_logs}"

    class Meta:
        permissions = [
            (_perm_view_all_user_logs, "Can view logs of all active users.")
        ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    log_date = models.DateField(default=datetime.date.today)
    logged_in = models.TimeField(default=time_now)
    break_duration = models.TimeField(null=True, blank=True)
    logged_out = models.TimeField(null=True, blank=True)

    # Can't be overwritten by application code.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("update", kwargs={"pk": str(self.id)})

    def __str__(self):
        return f"{self.user}, {self.log_date}, {self.logged_in}, {self.break_duration}, {self.logged_out}"


# See here for reason:
# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#substituting-a-custom-user-model
class User(AbstractUser):
    pass
