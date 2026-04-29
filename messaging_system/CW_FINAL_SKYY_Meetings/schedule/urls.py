from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/',    admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),   # gives us {% url 'logout' %}
    path('schedule/', include('meetings.urls', namespace='meetings')),
    path('',          RedirectView.as_view(url='/schedule/', permanent=False)),
]
