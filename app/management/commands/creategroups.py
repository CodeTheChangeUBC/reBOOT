"""
Create permission groups
Create permissions to models for a set of groups
"""
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from app.constants.perm_list import FRONTLINE, MANAGEMENT


def create_group(name, perms):
    group, created = Group.objects.get_or_create(name=name)
    for perm in perms:
        print(f'Adding permission with codname={perm}')
        permission = Permission.objects.get(codename=perm)
        if permission not in group.permissions.all():
            group.permissions.add(permission)


class Command(BaseCommand):
    help = 'Creates default permission groups for users'

    def handle(self, *args, **options):
        create_group('frontline', FRONTLINE)
        create_group('management', MANAGEMENT)

        print("Created new groups:", "frontline,", "management")
