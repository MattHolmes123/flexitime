from django import forms

from .models import FlexiTimeLog


def time_input_kwargs():
    return {
        'attrs': {'type': 'time', 'class': 'input is-small'},
        'format': '%H:%M'
    }


class EditFlexiTimeForm(forms.ModelForm):
    class Meta:
        model = FlexiTimeLog
        fields = ('logged_in', 'break_duration', 'logged_out')
        widgets = {
            'logged_in': forms.TimeInput(**time_input_kwargs()),
            'break_duration': forms.TimeInput(**time_input_kwargs()),
            'logged_out': forms.TimeInput(**time_input_kwargs()),
        }
