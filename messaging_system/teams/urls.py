from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings_page, name='settings_page'),
    path('', views.teams_page, name='teams_page'),
    path('<int:team_id>/', views.team_detail, name='team_detail'),
    path('<int:team_id>/schedule/', views.schedule_meeting, name='schedule_meeting'),
]