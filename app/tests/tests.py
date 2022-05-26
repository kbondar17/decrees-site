
# можно написать подобное
'''

from django.db import IntegrityError
from django.test import TestCase

from example.core.models import Team


class TeamTests(TestCase):
    def test_name_non_empty(self):
        constraint_name = "core_team_name_not_empty"
        with self.assertRaisesMessage(IntegrityError, constraint_name):
            Team.objects.create(name="")'''