from typing import Any, Dict
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.forms.models import BaseModelForm
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from . forms import GoalCreateForm, GoalUpdateForm
from . models import Goal, Employee, Manager
from user_profile.models import ManagerProfile


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
    

class GoalUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Goal
    form_class = GoalUpdateForm
    template_name = 'goals_management/update_goal.html'
    success_url = reverse_lazy('goal_list')   

    def get_initial(self):
        initial = super().get_initial()
        obj = self.get_object()
        initial["title"] = obj.title
        initial["status"] = obj.status
        initial["description"] = obj.description
        initial["start_date"] = obj.start_date
        initial["end_date"] = obj.end_date
        initial["priority"] = obj.priority
        initial["progress"] = obj.progress
        return initial
    

class GoalDetailView(LoginRequiredMixin, generic.DetailView):
    model = Goal
    template_name = 'goals_management/goal_detail.html' 

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['goal'] = get_object_or_404(Goal, id=self.kwargs['pk'])
        return context


class GoalDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Goal
    template_name = 'goals_management/goal_delete.html'
    success_url = reverse_lazy('goal_list')

    def form_valid(self, form):
        messages.success(self.request, _('Goal is deleted successfully'))
        return super().form_valid(form)

    def test_func(self) -> bool | None:
        obj = self.get_object()
        return obj.owner == self.request.user  
    


class DepartmentEmployeesListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    template_name = 'goals_management/employees_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        manager = get_object_or_404(Manager, user=self.request.user)
        queryset = Employee.objects.filter(manager=manager)
        return queryset

    def test_func(self) -> bool | None:
        return hasattr(self.request.user, "manager")
