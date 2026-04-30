from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from teams.models import Team
from .models import Department

@login_required
def home(request):
    all_teams = Team.objects.all()
    return render(request, 'organisation/home.html', {'all_teams': all_teams})

'''
dept_map = {}
for team in Team.objects.all():
    dept_name = team.department.name
    if dept_name not in dept_map:
        dept_map[dept_name] = []
    dept_map[dept_name].append(team)

    departments = []
for dept_name, teams in dept_map.items():
    departments.append({
        'name': dept_name,
        'teams': teams,
        'team_count': len(teams)
    })
'''

@login_required
def department_detail(request, department_name):
    teams = Team.objects.filter(department=department_name)   
    return render(request, 'organisation/department_detail.html', {'teams': teams, 
                                                                   'department_name':department_name})

@login_required
def department_list(request):
    all_teams = Team.objects.all()
    dept_map = {}
    for team in all_teams:
        dept_name = team.department or 'Unassigned'
        if dept_name not in dept_map:
            dept_map[dept_name] = {'name': dept_name, 'teams':[], 'team_count':0}
            dept_map[dept_name]['teams'].append(team)
            dept_map[dept_name]['team_count'] += 1

    departments = sorted(dept_map.values(), key=lambda x: x['name'])
    return render(request, 'organisation/department_list.html', {'departments': departments,
                                                                 })



@login_required
def dependencies_view(request):
    teams = Team.objects.all()
    return render(request, 'organisation/dependencies.html', {'all_teams': teams,
                                                              'selected_team':None,
                                                              'upstream_teams': [],
                                                              'downstram_teams': []}
                                                            ) 

@login_required
def team_dependencies_view(request, team_id):
    selected_team = get_object_or_404(Team, id=team_id)
    all_teams = Team.objects.all()

    return render(request, 'organisation/dependencies.html', {'all_teams': all_teams,
                                                            'selected_team':selected_team} )



@login_required
def team_type_view(request, team_type):
    teams = Team.objects.filter(team_type=team_type)
    return render(request, 'organisation/team_type.html', {'teams': teams, 'team_type': team_type}) 
