from main.services.overtime import OvertimeService

from .local_command import LocalCommandBase


class Command(LocalCommandBase):
    help = 'Creates a test admin user.'

    def handle(self, *args, **options):

        user = self.get_or_create_superuser('admin')

        overtime = OvertimeService(user)

        for day in overtime.get_this_week_as_date_list():
            self.create_test_log_for_day(user, day, 8)

            if day == overtime.today:
                return
