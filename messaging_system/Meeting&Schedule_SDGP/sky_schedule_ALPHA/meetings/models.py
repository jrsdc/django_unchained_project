from django.db import models
from django.contrib.auth.models import User


class Meeting(models.Model):
    MEETING_TYPES = [
        ('standup',    'Stand-up'),
        ('one_on_one', '1-on-1'),
        ('review',     'Review'),
        ('planning',   'Planning'),
        ('interview',  'Interview'),
        ('workshop',   'Workshop'),
        ('other',      'Other'),
    ]

    title        = models.CharField(max_length=255)
    meeting_type = models.CharField(max_length=20, choices=MEETING_TYPES, default='other')
    date         = models.DateField()
    start_time   = models.TimeField()
    end_time     = models.TimeField()
    description  = models.TextField(blank=True)
    location     = models.CharField(max_length=255, blank=True)
    created_by   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_meetings')
    attendees    = models.ManyToManyField(User, related_name='attending_meetings', blank=True)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.title} ({self.date})"

    def type_color(self):
        colors = {
            'standup':    '#9d4edd',
            'one_on_one': '#007aff',
            'review':     '#34c759',
            'planning':   '#ff9500',
            'interview':  '#ff3b30',
            'workshop':   '#5ac8fa',
            'other':      '#8e8e93',
        }
        return colors.get(self.meeting_type, '#8e8e93')
