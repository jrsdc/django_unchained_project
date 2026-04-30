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

        self.dept = Department.objects.create(
            name='Engineering',
            specialisation='Frontend developmment',
            status='Active',
            leader=self.user,
        )

    def test_home_page_loads(self):
            response = self.client.get('/organisation/')
            self.assertEqual(response.status_code,200)

    def test_home_show_teams(self):
            response = self.client.get('/organisation/')
            self.assertContains(response,'Team 1')

    def test_department_list_loads(self):
            response = self.client.get('/organisation/departments/')
            self.assertEqual(response.status_code,200)

    def test_department_list_shows_department(self):
            response = self.client.get('/organisation/departments/')
            self.assertContains(response,'Engineering')        

    def test_department_detail_loads(self):
            response = self.client.get('/organisation/departments/Engineering/')
            self.assertEqual(response.status_code,200)

    def test_dependencies_page_loads(self):
            response = self.client.get('/organisation/dependencies/')
            self.assertEqual(response.status_code,200)


    def test_department_details_shows_teams(self):
            response = self.client.get('/organisation/departments/Engineering/')
            self.assertContains(response,'Team 1')

    def test_dependencies_with_team(self):
            response = self.client.get(f'/organisation/dependencies/{self.team1.id}/')
            self.assertEqual(response.status_code, 200)        

    def test_login_required_home(self):
           self.client.logout()
           response = self.client.get('/organisation/')
           self.assertEqual(response.status_code, 302)

    def test_department_str_model(self):
           self.assertEqual(str(self.dept), 'Engineering')