import calendar
from collections import defaultdict
from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MeetingForm
from .models import Meeting


@login_required
def schedule(request):
    today = date.today()

    year  = int(request.GET.get('year',  today.year))
    month = int(request.GET.get('month', today.month))
    day   = int(request.GET.get('day',   today.day if (year == today.year and month == today.month) else 1))

    max_day = calendar.monthrange(year, month)[1]
    day = min(day, max_day)

    selected_date = date(year, month, day)

    month_meetings = Meeting.objects.filter(
        date__year=year, date__month=month
    ).filter(
        Q(created_by=request.user) | Q(attendees=request.user)
    ).distinct().select_related('created_by').prefetch_related('attendees')

    day_meetings = month_meetings.filter(date=selected_date)

    cal   = calendar.Calendar(firstweekday=0)
    weeks = cal.monthdatescalendar(year, month)

    # Group meetings by date so the template can render them without JavaScript
    meetings_by_date = defaultdict(list)
    for m in month_meetings:
        meetings_by_date[m.date].append(m)

    weeks_with_meetings = [
        [(d, meetings_by_date.get(d, [])) for d in week]
        for week in weeks
    ]

    prev_year,  prev_month = (year - 1, 12) if month == 1  else (year, month - 1)
    next_year,  next_month = (year + 1, 1)  if month == 12 else (year, month + 1)

    context = {
        'year':                year,
        'month':               month,
        'month_name':          calendar.month_name[month],
        'day':                 day,
        'selected_date':       selected_date,
        'weeks_with_meetings': weeks_with_meetings,
        'today':               today,
        'day_meetings':        day_meetings,
        'prev_year':           prev_year,  'prev_month': prev_month,
        'next_year':           next_year,  'next_month': next_month,
        'new_form':            MeetingForm(initial={'date': selected_date}),
        'months_list':         [(i, calendar.month_name[i]) for i in range(1, 13)],
        'year_range':          range(today.year - 2, today.year + 5),
        'weekdays':            ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    }
    return render(request, 'meetings/schedule.html', context)


@login_required
def create_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.created_by = request.user
            meeting.save()
            form.save_m2m()
            d = meeting.date
            return redirect(f'/schedule/?year={d.year}&month={d.month}&day={d.day}')
    return redirect('schedule')


@login_required
def edit_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id, created_by=request.user)
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            d = meeting.date
            return redirect(f'/schedule/?year={d.year}&month={d.month}&day={d.day}')
    else:
        form = MeetingForm(instance=meeting)
    return render(request, 'meetings/edit_meeting.html', {'form': form, 'meeting': meeting})


@login_required
def delete_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id, created_by=request.user)
    d = meeting.date
    meeting.delete()
    return redirect(f'/schedule/?year={d.year}&month={d.month}&day={d.day}')


@login_required
def meeting_detail_api(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    return JsonResponse(_meetings_json([meeting])[0])
