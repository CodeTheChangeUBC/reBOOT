"""
Create permission groups
Create permissions to models for a set of groups
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from app.models import Item
from app.constants.perm_list import FRONTLINE, MANAGEMENT


class Command(BaseCommand):
    help = 'Creates default permission groups for users'

    def handle(self, *args, **options):
        frontline, created = Group.objects.get_or_create(name='frontline')
        for perm in FRONTLINE:
            permission = Permission.objects.get(codename=perm)
            if not permission in frontline.permissions.all():
                frontline.permissions.add(permission)
        management, created = Group.objects.get_or_create(name='management')
        for perm in MANAGEMENT:
            permission = Permission.objects.get(codename=perm)
            if not permission in management.permissions.all():
                management.permissions.add(permission)

        print("Created new groups:", "frontline,", "management")
