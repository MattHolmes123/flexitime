from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class FlexiTimeLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    logged_in = models.TimeField()
    break_duration = models.TimeField(null=True, blank=True)
    logged_out = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('update', kwargs={'pk': str(self.id)})

    def __str__(self):
        return f'{self.user}, {self.logged_in}, {self.break_duration}, {self.logged_out}'

