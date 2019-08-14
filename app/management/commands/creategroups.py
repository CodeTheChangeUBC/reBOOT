"""
Create permission groups
Create permissions to models for a set of groups
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from app.models import Item


class Command(BaseCommand):
    help = 'Creates default permission groups for users'

    def handle(self, *args, **options):
        volunteer_perm_list = [
            'add_donation',
            'change_donation',
            'delete_donation',
            'view_donation',
            'add_donor',
            'change_donor',
            'delete_donor',
            'view_donor',
            'add_item',
            'change_item',
            'delete_item',
            'view_item',
            'add_itemdevice',
            'change_itemdevice',
            'delete_itemdevice',
            'add_itemdevicetype',
            'change_itemdevicetype',
            'delete_itemdevicetype'
        ]
        volunteer, created = Group.objects.get_or_create(name='volunteer')

        for perm in volunteer_perm_list:
            volunteer.permissions.add(Permission.objects.get(codename=perm))
