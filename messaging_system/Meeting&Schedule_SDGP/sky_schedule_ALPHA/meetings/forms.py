from django import forms
from .models import Meeting
from django.contrib.auth.models import User


class MeetingForm(forms.ModelForm):
    attendees = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model  = Meeting
        fields = ['title', 'meeting_type', 'date', 'start_time',
                  'end_time', 'location', 'description', 'attendees']
        widgets = {
            'date':       forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time':   forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
