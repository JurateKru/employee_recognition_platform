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


class GoalUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Goal
        fields =('title', 'description', 'start_date', 'end_date', 'priority', 'status', 'progress')
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),            
        }


class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields =('employee', 'goals_achievment', 'goals_review', 'teamwork', 'teamwork_review', 'innovation', 'innovation_review', 'work_ethics', 'work_ethics_review', 'total_review')


class ReviewUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ('employee','goals_achievment', 'goals_review', 'teamwork', 'teamwork_review', 'innovation', 'innovation_review', 'work_ethics', 'work_ethics_review', 'total_review')


class GoalJournalForm(forms.ModelForm):
    journal = forms.CharField(widget=forms.Textarea(attrs={'class': 'small-input'}))

    class Meta:
        model = models.GoalJournal
        fields = ('journal', 'goal', 'owner')
        widgets = {
            'goal': forms.HiddenInput(),
            'owner': forms.HiddenInput(),
        }
