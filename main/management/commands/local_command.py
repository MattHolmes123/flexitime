import datetime
from typing import Callable

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from main.models import FlexiTimeLog

CreateUser = Callable[[str, str, str], User]


# See here for more information
# https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/
class LocalCommandBase(BaseCommand):
    
    user_model = get_user_model()
    
    def handle(self, *args, **options):
        raise NotImplementedError("Derived class must implement `handle` method.")

    def get_or_create_user(self, username: str) -> User:
        return self._create_user(username, self.user_model.objects.create_user)
    
    def get_or_create_superuser(self, username: str) -> User:
        return self._create_user(username, self.user_model.objects.create_superuser)

    def _create_user(self, username: str, create_user_func: CreateUser) -> User:
        """Either loads or creates a user using the supplied create_user_func.

        :param username: Username to get / create
        :param create_user_func: Function to create the user
        :return: User model
        """

        try:
            user = self.user_model.objects.get(username=username)
            self.stdout.write(f'Loaded test user {username}.')

        except self.user_model.DoesNotExist:
            user = create_user_func(username, f'{username}@email.com', username)
            self.stdout.write(f'Created test user {username}.')

        return user

    def create_test_log_for_day(self, user: User, log_date: datetime.date, log_in_hour: int) -> None:
        """Create a FlexiTimeLog entry, used when creating test data.

        :param user: User instance
        :param log_date: Log date
        :param log_in_hour: how user logged in.
        :return: None
        """

        log, created = FlexiTimeLog.objects.get_or_create(
            user=user,
            log_date=log_date,
            defaults={
                'logged_in': datetime.time(log_in_hour, 30, 0),
                'break_duration': datetime.time(0, 30, 0),
                'logged_out': datetime.time(17, 30, 0)
            }
        )

        if created:
            self.stdout.write(f'Created log for following date: {log_date}')
        else:
            self.stdout.write(f'loaded record: {log}')
