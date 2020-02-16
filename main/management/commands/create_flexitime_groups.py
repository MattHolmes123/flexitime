from django.contrib.auth.models import Group, Permission

from .local_command import LocalCommandBase


class Command(LocalCommandBase):
    help = 'Creates a test admin user.'

    def handle(self, *args, **options):

        all_logs_perm = Permission.objects.get(codename='view_all_user_logs')

        manager, created = Group.objects.get_or_create(
            name='Manager',
            defaults={'name': 'Manager'}
        )

        self.stdout.write(f'Manager group {"created" if created else "updated"}')

        staff, created = Group.objects.get_or_create(
            name='Staff',
            defaults={'name': 'Staff'}
        )

        self.stdout.write(f'Staff group {"created" if created else "updated"}')

        manager.permissions.set((all_logs_perm,))
        manager.save()
