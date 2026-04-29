from django.contrib import admin
from .models import Meeting

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'start_time', 'end_time', 'meeting_type', 'location')
    list_filter  = ('meeting_type', 'date')
    search_fields = ('title', 'description', 'location')
