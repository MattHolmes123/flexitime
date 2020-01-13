from django.db import migrations

# See below page for example of forwards_func / reverse_func
# https://docs.djangoproject.com/en/3.0/ref/migration-operations/#runpython

# Also have a read of this:
# https://docs.djangoproject.com/en/2.2/ref/contrib/contenttypes/


def forwards_func(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    all_logs_perm = Permission.objects.get(codename='view_all_user_logs')

    db_alias = schema_editor.connection.alias

    manager = Group.objects.using(db_alias).create(name='Manager')
    Group.objects.using(db_alias).create(name='Staff')

    manager.permissions.set((all_logs_perm,))
    manager.save()


def reverse_func(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    db_alias = schema_editor.connection.alias

    Group.objects.using(db_alias).filter(name="Manager").delete()
    Group.objects.using(db_alias).filter(name="Staff").delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func)
    ]
