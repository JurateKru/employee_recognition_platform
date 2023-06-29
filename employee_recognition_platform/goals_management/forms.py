from django import forms
from . import models


class DateInput(forms.DateInput):
    input_type = 'date'


class GoalCreateForm(forms.ModelForm):
    class Meta:
        model = models.Goal
        fields =('title', 'description', 'start_date', 'end_date', 'priority', 'status', 'progress')
        widgets = {
            'owner': forms.HiddenInput(),   
            'start_date': DateInput(),
            'end_date': DateInput(),
        }

