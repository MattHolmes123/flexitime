from django.core.management.base import BaseCommand, CommandError
from main.models import FlexiTimeLog

# See here for more information
# https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/


class Command(BaseCommand):
    help = 'test command used for testing django stuff (e.g. ORM queries)'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):

        log_times = FlexiTimeLog.objects.all()

        for log in log_times:
            self.stdout.write(
                self.style.SUCCESS(
                    log.calculate_overtime()
                )
            )
