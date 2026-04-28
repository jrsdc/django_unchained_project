from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    status_choices = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    name = models.CharField(max_length=100, unique=True)
    ##Specialisation has been added as it was missing previously and is a requirement for CW2 
    specialisation = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=status_choices, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    ##Leader field previously missing and is a reuqienent for the CW
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='department_leader')

    ##this orders from A-Z by name
    class Meta: ordering = ['name']

    ##Customer helper method that finds all teams in the department
    ##Customer helper method that finds all teams in the department
    def get_teams(self):
        from teams.models import Team
        return Team.objects.filter(department=self)

    def __str__(self):
        return f"{self.name}"
    
    def get_team_count(self):
        return self.get_teams().count()