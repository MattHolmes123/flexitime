import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
WORKING_DAY = datetime.timedelta(hours=7.5)


class FlexiTimeLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    logged_in = models.TimeField()
    break_duration = models.TimeField(null=True, blank=True)
    logged_out = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def login(self, logged_in: datetime.time = None) -> None:

        if logged_in is None:
            self.logged_in = timezone.now().time()

        self.save(update_fields=['logged_in'])

    # TODO - Remove all the fat logic
    def calculate_overtime(self) -> datetime.timedelta:
        time_in = time_as_td(self.logged_in)
        lunch_break = time_as_td(self.break_duration)
        time_out = time_as_td(self.logged_out)

        if not all([time_in, time_out, lunch_break]):
            return datetime.timedelta(0)

        return ((time_out - time_in) - lunch_break) - WORKING_DAY

    def get_absolute_url(self):
        return reverse('update', kwargs={'pk': str(self.id)})

    def __str__(self):
        return f'{self.user}, {self.logged_in}, {self.break_duration}, {self.logged_out}'


def time_as_td(dt: datetime.time) -> datetime.timedelta:

    return datetime.timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
