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
from . forms import GoalCreateForm, GoalUpdateForm, ReviewCreateForm, ReviewUpdateForm
from . models import Goal, Employee, Manager, Review


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
    success_url = reverse_lazy('goal_list')

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
    template_name = 'goals_management/delete_goal.html'
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
    

class DepartmentGoalsListView(LoginRequiredMixin, generic.ListView):
    template_name = 'goals_management/employee_goals_list.html'
    context_object_name = 'goals'

    def get_queryset(self):
        manager = get_object_or_404(Manager, user=self.request.user)
        employee = manager.employees.get(id=self.kwargs['pk'])
        queryset = Goal.objects.filter(owner__employee=employee)
        return queryset

    def test_func(self) -> bool | None:
        return hasattr(self.request.user, "manager")
    

class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Employee
    template_name = 'goals_management/employee_detail.html' 

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['employee'] = get_object_or_404(Employee, id=self.kwargs['pk'])
        return context


class ReviewCreateView(LoginRequiredMixin, generic.CreateView):
    model = Review
    form_class = ReviewCreateForm
    template_name = 'goals_management/create_review.html'
    success_url = reverse_lazy('employees_list')

    def get_initial(self) -> Dict[str, Any]:
        initial =  super().get_initial()
        manager = get_object_or_404(Manager, user=self.request.user)
        initial['manager'] = manager
        initial['employee'] = get_object_or_404(Employee, id=self.kwargs['pk'])
        return initial
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        manager = get_object_or_404(Manager, user=self.request.user)
        form.instance.manager = manager
        messages.success(self.request, _('Review is created successfully!'))
        return super().form_valid(form)
    

class DepartmentReviewsListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    template_name = 'goals_management/department_reviews.html'
    context_object_name = 'department_reviews'

    def get_queryset(self):
        queryset = Review.objects.filter(manager=self.request.user.manager)
        return queryset

    def test_func(self) -> bool | None:
        return hasattr(self.request.user, "manager")
    

class ReviewDetailView(LoginRequiredMixin, generic.DetailView):
    model = Review
    template_name = 'goals_management/review_detail.html' 

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['review'] = get_object_or_404(Review, id=self.kwargs['pk'])
        return context


class ReviewUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Review
    form_class = ReviewUpdateForm
    template_name = 'goals_management/update_review.html'
    success_url = reverse_lazy('department_reviews')   

    def get_initial(self):
        initial = super().get_initial()
        obj = self.get_object()
        initial["goals achievment"] = obj.goals_achievment
        initial["goals review"] = obj.goals_review
        initial["teamwork"] = obj.teamwork
        initial["teamwork review"] = obj.teamwork_review
        initial["innovation"] = obj.innovation
        initial["innovation_review"] = obj.innovation_review
        initial["work ethics"] = obj.work_ethics
        initial["work ethics review"] = obj.work_ethics_review
        initial["total review"] = obj.total_review
        return initial
    

class ReviewDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Review
    template_name = 'goals_management/delete_review.html'
    success_url = reverse_lazy('department_reviews')

    def form_valid(self, form):
        messages.success(self.request, _('Review is deleted successfully'))
        return super().form_valid(form)

    def test_func(self) -> bool | None:
        obj = self.get_object()
        return obj.manager == self.request.user  
