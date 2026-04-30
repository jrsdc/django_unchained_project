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

        self.team2 = Team.objects.create(
            name='Team 2',
            department='Engineering',
            manager='Dhon Jouble',
            description='The test engineering team 2',
            skills='Python, Django, Java',
            email='secomd@sky.com',
            downstream_dependencies='',
            upstream_dependencies='Team 1',
        )

        self.team3 = Team.objects.create(
            name='Team 3',
            department='Ui/Ux',
            manager='Third Man',
            description='The test Ui/Ux team',
            skills='Python, Django, Java',
            email='third@sky.com',
            downstream_dependencies='',
            upstream_dependencies='',
        )