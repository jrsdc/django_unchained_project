from django.db import models


class Meeting(models.Model):
    MEETING_TYPES = [
        ('internal', 'Internal Review'),
        ('client', 'Client Meeting'),
        ('brainstorm', 'Brainstorming'),
    ]

    title = models.CharField(max_length=200)
    meeting_type = models.CharField(max_length=20, choices=MEETING_TYPES, default='internal')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.date}"

    class Meta:
        ordering = ['date', 'start_time']
