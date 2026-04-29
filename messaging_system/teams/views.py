from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Team

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def teams_page(request):
    search = request.GET.get("search", "").strip()
    department = request.GET.get("department", "").strip()
    specialisation = request.GET.get("specialisation", "").strip()
    manager = request.GET.get("manager", "").strip()

    teams = Team.objects.all().order_by("department", "name")

    if search:
        teams = teams.filter(
            Q(name__icontains=search) |
            Q(manager__icontains=search) |
            Q(department__icontains=search) |
            Q(skills__icontains=search) |
            Q(team_type__icontains=search) |
            Q(description__icontains=search) |
            Q(upstream_dependencies__icontains=search) |
            Q(downstream_dependencies__icontains=search)
        )

    if department:
        teams = teams.filter(department=department)

    if specialisation:
        teams = teams.filter(team_type=specialisation)

    if manager:
        teams = teams.filter(manager=manager)

    departments = Team.objects.exclude(department="").values_list("department", flat=True).distinct().order_by("department")
    specialisations = Team.objects.exclude(team_type="").values_list("team_type", flat=True).distinct().order_by("team_type")
    managers = Team.objects.exclude(manager="").values_list("manager", flat=True).distinct().order_by("manager")

    return render(request, "teams/teams_page.html", {
        "teams": teams,
        "search": search,
        "departments": departments,
        "specialisations": specialisations,
        "managers": managers,
        "selected_department": department,
        "selected_specialisation": specialisation,
        "selected_manager": manager,
    })


@login_required
def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    return render(request, "teams/team_detail.html", {
        "team": team,
    })


@login_required
def schedule_meeting(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    submitted = False

    if request.method == "POST":
        submitted = True

    return render(request, "teams/schedule_meeting.html", {
        "team": team,
        "submitted": submitted,
    })

@login_required
def dashboard(request):
    total_teams = Team.objects.count()
    total_departments = Team.objects.values("department").distinct().count()
    total_managers = Team.objects.values("manager").distinct().count()

    recent_teams = Team.objects.all().order_by("department", "name")[:5]

    return render(request, "teams/dashboard.html", {
        "total_teams": total_teams,
        "total_departments": total_departments,
        "total_managers": total_managers,
        "recent_teams": recent_teams,
    })

@login_required
def settings_page(request):
    user = request.user

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "profile":
            user.first_name = request.POST.get("first_name", "")
            user.last_name = request.POST.get("last_name", "")
            user.email = request.POST.get("email", "")
            user.save()
            messages.success(request, "Profile updated successfully.")

        elif form_type == "password":
            password_form = PasswordChangeForm(user, request.POST)

            if password_form.is_valid():
                changed_user = password_form.save()
                update_session_auth_hash(request, changed_user)
                messages.success(request, "Password changed successfully.")
            else:
                messages.error(request, "Password change failed. Please check the form.")

    password_form = PasswordChangeForm(user)

    return render(request, "teams/settings.html", {
        "password_form": password_form,
    })