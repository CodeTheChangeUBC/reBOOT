from django.contrib.auth.models import Group
from django.test import TestCase

from app.constants.perm_list import FRONTLINE, MANAGEMENT
from app.management.commands.creategroups import Command


class CreateGroupsCommandTestCase(TestCase):
    def setUp(self):
        command = Command()

        command.handle()

        self.frontline_group = Group.objects.get(name="frontline")
        self.management_group = Group.objects.get(name="management")

    def verifyGroup(self, group, codenames):
        self.assertIsNotNone(group)

        for codename in codenames:
            permission = group.permissions.get(codename=codename)

            self.assertIsNotNone(permission, codename)

    def test_handle_creates_frontline_group(self):
        self.verifyGroup(self.frontline_group, FRONTLINE)

    def test_handle_creates_management_group(self):
        self.verifyGroup(self.management_group, MANAGEMENT)
