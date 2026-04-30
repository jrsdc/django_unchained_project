from django.test import TestCase, Client
from django.contrib.auth.models import User
from teams.models import Team
from organisation.models import Department

class OrganisationTests(TestCase):
    def setUp(self):
        # Test user to log in
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.client.login(username='testuser', password='testpass123')

        #creating test teams
        self.team1 = Team.objects.create(
            name='Team 1',
            department='Engineering',
            manager='John Double',
            description='The test engineering team',
            skills='Python, Django',
            email='first@sky.com',
            downstream_dependencies='Team 2',
            upstream_dependencies='',
        )