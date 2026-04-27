from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    team_type = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    description = models.TextField()
    skills = models.CharField(max_length=255, help_text="Separate skills with commas")
    upstream_dependencies = models.CharField(max_length=255, blank=True)
    downstream_dependencies = models.CharField(max_length=255, blank=True)
    email = models.EmailField()
    repository = models.URLField(blank=True)

    @property
    def skill_list(self):
        return [skill.strip() for skill in self.skills.split(",") if skill.strip()]

    def __str__(self):
        return self.name

