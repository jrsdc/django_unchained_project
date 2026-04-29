from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from teams.models import Team
from .models import Department

@login_required
def home(request):
    all_teams = Team.objects.all()
    return render(request, 'organisation/home.html', {'all_teams': all_teams})

