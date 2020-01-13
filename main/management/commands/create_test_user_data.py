from django.contrib.auth.models import User, Group

from main.services.overtime import OvertimeService
from .local_command import LocalCommandBase


class Command(LocalCommandBase):
    help = 'Command used to create test users when developing locally'

    def handle(self, *args, **options):
        users = self.get_staff()

        for user_num, user in enumerate(users):
            self._create_overtime_for_user(user, user_num)

        manager = self.get_manager()
        self._create_overtime_for_user(manager)

    def _create_overtime_for_user(self, user: User, user_num: int = 0) -> None:

        # Just to get a bit of variation
        log_in_hour = 7 + user_num
        overtime = OvertimeService(user)

        for day in overtime.get_this_week_as_date_list():
            self.create_test_log_for_day(user, day, log_in_hour)

            if day == overtime.today:
                return

    def get_staff(self) -> list:
        """Either creates or loads test users."""

        staff_group = Group.objects.get_by_natural_key('Staff')
        test_users = ['test_user_one', 'test_user_two', 'test_user_three']
        return_users = []

        for username in test_users:
            user = self.get_or_create_user(username)
            user.groups.set((staff_group,))
            user.save()
            return_users.append(user)

        return return_users

    def get_manager(self) -> User:
        manager_group = Group.objects.get_by_natural_key('Manager')
        user = self.get_or_create_user('manager_one')
        user.groups.set((manager_group,))
        user.save()

        return user
