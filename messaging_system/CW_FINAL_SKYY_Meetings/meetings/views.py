import calendar
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Meeting


def calendar_view(request):
    today = date.today()

    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # Clamp month to 1-12
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    # All meetings for this month
    meetings_qs = Meeting.objects.filter(date__year=year, date__month=month)

    meetings_by_day = {}
    for m in meetings_qs:
        meetings_by_day.setdefault(m.date.day, []).append(m)

    # Build calendar weeks (Monday first)
    cal = calendar.Calendar(firstweekday=0)
    calendar_weeks = []
    for week in cal.monthdatescalendar(year, month):
        week_data = []
        for d in week:
            week_data.append({
                'day': d.day,
                'date': d,
                'is_current_month': d.month == month,
                'is_today': d == today,
                'meetings': meetings_by_day.get(d.day, []) if d.month == month else [],
            })
        calendar_weeks.append(week_data)

    # Prev / next month
    prev_month = month - 1 if month > 1 else 12
    prev_year  = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year  = year if month < 12 else year + 1

    month_name = calendar.month_name[month]

    # Sidebar: show today's info when viewing the current month
    viewing_current = (year == today.year and month == today.month)
    selected_day_name  = today.strftime('%A') if viewing_current else calendar.month_name[month]
    selected_date_str  = today.strftime('%-d %B %Y') if viewing_current else f'{month_name} {year}'
    today_meetings     = meetings_by_day.get(today.day, []) if viewing_current else []

    # Month/year options for dropdowns
    months = [(i, calendar.month_name[i]) for i in range(1, 13)]
    years  = list(range(today.year - 3, today.year + 5))

    context = {
        'year': year,
        'month': month,
        'month_name': month_name,
        'calendar_weeks': calendar_weeks,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'today': today,
        'selected_day_name': selected_day_name,
        'selected_date_str': selected_date_str,
        'today_meetings': today_meetings,
        'months': months,
        'years': years,
    }
    return render(request, 'calender.html', context)


def meeting_create(request):
    if request.method == 'POST':
        Meeting.objects.create(
            title=request.POST['title'],
            meeting_type=request.POST['meeting_type'],
            date=request.POST['date'],
            start_time=request.POST['start_time'],
            end_time=request.POST['end_time'],
            location=request.POST.get('location', ''),
            description=request.POST.get('description', ''),
        )
        return redirect('meetings:calendar')

    context = {
        'action': 'Create',
        'meeting': None,
        'form_action': reverse('meetings:create'),
        'today_str': date.today().strftime('%Y-%m-%d'),
    }
    return render(request, 'schedule_base.html', context)


def meeting_edit(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)

    if request.method == 'POST':
        meeting.title        = request.POST['title']
        meeting.meeting_type = request.POST['meeting_type']
        meeting.date         = request.POST['date']
        meeting.start_time   = request.POST['start_time']
        meeting.end_time     = request.POST['end_time']
        meeting.location     = request.POST.get('location', '')
        meeting.description  = request.POST.get('description', '')
        meeting.save()
        return redirect('meetings:calendar')

    context = {
    'action': 'Edit',
    'meeting': meeting,
    'form_action': reverse('meetings:edit', kwargs={'pk': pk}),
    'delete_url': reverse('meetings:delete', kwargs={'pk': pk}),
    'today_str': date.today().strftime('%Y-%m-%d'),

    }
    return render(request, 'schedule_base.html', context)


def meeting_delete(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    if request.method == 'POST':
        meeting.delete()
    return redirect('meetings:calendar')
