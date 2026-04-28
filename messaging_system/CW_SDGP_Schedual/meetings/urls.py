from django.urls import path
from . import views

urlpatterns = [
    path('',                              views.schedule,           name='schedule'),
    path('create/',                       views.create_meeting,     name='create_meeting'),
    path('edit/<int:meeting_id>/',        views.edit_meeting,       name='edit_meeting'),
    path('delete/<int:meeting_id>/',      views.delete_meeting,     name='delete_meeting'),
    path('api/<int:meeting_id>/',         views.meeting_detail_api, name='meeting_detail_api'),
]
