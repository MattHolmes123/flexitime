from django import forms

from .models import FlexiTimeLog


class EditFlexiTimeForm(forms.ModelForm):
    class Meta:
        model = FlexiTimeLog
        fields = ('logged_in', 'break_duration', 'logged_out')
        widgets = {
            'logged_in': forms.TimeInput(format='%H:%M'),
            'break_duration': forms.TimeInput(format='%H:%M'),
            'logged_out': forms.TimeInput(format='%H:%M'),
        }
