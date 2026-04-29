from django.contrib import admin
from .models import Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialisation', 'status', 'leader', 'created_at')
    search_fields = ('name', 'specialisation', 'leader')
    list_filter = ('status', 'created_at')

