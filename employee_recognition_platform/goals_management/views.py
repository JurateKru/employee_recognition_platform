from typing import Any, Dict
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.forms.models import BaseModelForm
from django.db.models import Q
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


class GoalListView(generic.ListView):
    model = Goal
    template_name = 'goals_management/goal_list.html'
    context_object_name = 'goal_list'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        return qs.filter(owner=user)


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
    

class GoalDetailView(LoginRequiredMixin, generic.DetailView):
    model = Goal
    template_name = 'goals_management/goal_detail.html' 

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['goal'] = get_object_or_404(Goal, id=self.kwargs['pk'])
        return context
    

