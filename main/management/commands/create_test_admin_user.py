import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from main.models import FlexiTimeLog
from main.services.overtime import OvertimeService

# See here for more information
# https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/


class Command(BaseCommand):
    help = 'test command used for testing django stuff (e.g. ORM queries)'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        # Note: This command is never for production (only local).
        user_model = get_user_model()

        try:
            user = user_model.objects.get(username='admin')
            self.stdout.write('Loaded test admin user.')
        except ObjectDoesNotExist:
            user = user_model.objects.create_superuser('admin', 'admin@email.com', 'admin')
            self.stdout.write('Created test admin user.')

        overtime = OvertimeService(user)

        for day in overtime.get_this_week_as_date_list():
            log, created = FlexiTimeLog.objects.get_or_create(
                user=user,
                log_date=day,
                defaults={
                    'logged_in': datetime.time(7, 30, 0),
                    'break_duration': datetime.time(0, 30, 0),
                    'logged_out': datetime.time(17, 30, 0)
                }
            )

            if created:
                self.stdout.write(f'Created log for following date: {day}')
            else:
                self.stdout.write(f'loaded record: {log}')

            if day == overtime.today:
                return
