from typing import Any, Dict
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from . forms import GoalCreateForm
from . models import Goal


def index(request):
    return render(request, 'goals_management/index.html')

def ismart(request):
    return render(request, 'goals_management/ismart.html')

class GoalCreateView(LoginRequiredMixin, generic.CreateView):
    model = Goal
    form_class = GoalCreateForm
    template_name = 'goals_management/create_goal.html'
    success_url = reverse_lazy('index')

    def get_initial(self) -> Dict[str, Any]:
        initial =  super().get_initial()
        initial['owner'] = self.request.user
        return initial
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.owner = self.request.user
        messages.success(self.request, _('Goal is created successfully!'))
        return super().form_valid(form)

