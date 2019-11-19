from django import forms


class EditFlexiTimeForm(forms.Form):
    logged_in = forms.TimeField(help_text='Enter the time you logged in')
    break_duration = forms.TimeField(help_text='Enter the time you had for lunch')
    logged_out = forms.TimeField(help_text='Enter the time you logged out')
