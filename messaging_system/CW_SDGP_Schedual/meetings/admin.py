from django.contrib import admin
from .models import Meeting

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display  = ('title', 'meeting_type', 'date', 'start_time', 'created_by')
    list_filter   = ('meeting_type', 'date')
    search_fields = ('title', 'description')
