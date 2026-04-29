from django.urls import path
from . import views

app_name = 'meetings'

urlpatterns = [
    path('',                         views.calendar_view,  name='calendar'),
    path('meeting/create/',          views.meeting_create, name='create'),
    path('meeting/<int:pk>/edit/',   views.meeting_edit,   name='edit'),
    path('meeting/<int:pk>/delete/', views.meeting_delete, name='delete'),
]

