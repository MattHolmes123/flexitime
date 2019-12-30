from django import forms

from .models import FlexiTimeLog
from typing_extensions import TypedDict


# Example of using a TypedDict class.
class TimeInputData(TypedDict):
    attrs: dict
    format: str


def time_input_kwargs() -> TimeInputData:
    return {"attrs": {"type": "time", "class": "input is-small"}, "format": "%H:%M"}


class EditFlexiTimeForm(forms.ModelForm):
    class Meta:
        model = FlexiTimeLog
        fields = ("logged_in", "break_duration", "logged_out")
        widgets = {
            "logged_in": forms.TimeInput(**time_input_kwargs()),
            "break_duration": forms.TimeInput(**time_input_kwargs()),
            "logged_out": forms.TimeInput(**time_input_kwargs()),
        }
