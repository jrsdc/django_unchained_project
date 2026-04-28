
from . import views
from django.urls import path

from messaging_system.teams import views

urlpatterns = [
    path('', views.home, name='home'),
    path('departments/', views.department_list, name='department_list'),
    path('departments/<str:department_name>/', views.department_detail, name='department_detail'),
    path('dependencies/', views.dependencies_view, name='dependencies'),
    path('dependencies/<int:team_id>/', views.team_dependencies_view, name='team_dependencies'),
    path('team-type/<str:team_type>/', views.team_type_view, name='team_type'),
   

]
