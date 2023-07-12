from django.test import TestCase

from app.management.commands.creategroups import Command
from app.constants.perm_list import FRONTLINE, MANAGEMENT
from django.contrib.auth.models import Group


class CreateGroupsCommandTestCase(TestCase):
    def setUp(self):
        command = Command()

        command.handle()

        self.frontline_group = Group.objects.get(name="frontline")
        self.management_group = Group.objects.get(name="management")

    def test_handle_creates_frontline_group(self):
        self.assertIsNotNone(self.frontline_group)
        for codename in FRONTLINE:
            permission = self.frontline_group.permissions.get(codename=codename)

            self.assertIsNotNone(permission, codename)

    def test_handle_creates_management_group(self):
        self.assertIsNotNone(self.management_group)
        for codename in MANAGEMENT:
            permission = self.management_group.permissions.get(codename=codename)

            self.assertIsNotNone(permission, codename)
