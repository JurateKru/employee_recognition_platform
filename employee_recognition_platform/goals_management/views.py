from typing import Any, Dict
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.forms.models import BaseModelForm
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from . forms import GoalCreateForm, GoalUpdateForm, ReviewCreateForm, ReviewUpdateForm, GoalJournalForm
from . models import Goal, Employee, Manager, Review
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from django.db import models
import matplotlib.ticker as ticker
import threading


def index(request):
    return render(request, 'goals_management/index.html')


def search_view(request):
    query = request.GET.get('query')
    if query:
        goal_results = Goal.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        review_results = Review.objects.filter(Q(goals_achievment__icontains=query) | Q(teamwork__icontains=query) | Q(innovation__icontains=query) | Q(work_ethics__icontains=query))
        results = list(goal_results) + list(review_results)
    else:
        results = []
    return render(request, 'goals_management/search_results.html', {'results': results, 'query': query})


def smart(request):
    grid_data = [
        ['S', 'M', 'A', 'R', 'T'],
        ['Specific', 'Measurable', 'Attainable', 'Relevant', 'Time-bound'],
        ['Define your goal in detail. Be as specific as possible',
         'Decide how you wil measure success',
         'Set realistic goals that challenge you, but are achievable',
         'Ensure your goal is results-oriented',
         'Set a clear deadline and monitos your progress'],
        ['G', 'O', 'A', 'L', 'S'],
    ]
    return render(request, 'goals_management/smart.html', {'grid_data': grid_data})


class GoalListView(generic.ListView):
    model = Goal
    template_name = 'goals_management/goal_list.html'
    context_object_name = 'goal_list'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status) 
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
    
    def get_success_url(self) -> str:
        return reverse('goal_detail', kwargs={'pk':self.get_object().pk})


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
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status')
        return context

    def test_func(self) -> bool | None:
        return hasattr(self.request.user, "manager")
    

class DepartmentGoalsListView(LoginRequiredMixin, generic.ListView):
    template_name = 'goals_management/employee_goals_list.html'
    context_object_name = 'goals'

    def get_queryset(self):
        manager = get_object_or_404(Manager, user=self.request.user)
        employee = manager.employees.get(id=self.kwargs['pk'])
        priority = self.request.GET.get('priority')
        status = self.request.GET.get('status')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        queryset = Goal.objects.filter(owner__employee=employee)
        if priority is not None and priority != 'all':
            queryset = queryset.filter(priority=priority)
        if status is not None and status != 'all':
            queryset = queryset.filter(status=status)
        if start_date and end_date:
            queryset = queryset.filter(
                Q(start_date__gte=start_date) & Q(end_date__lte=end_date)
            )
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
        if "pk" in self.kwargs:
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
        year_filter = self.request.GET.get('year')
        employee_filter = self.request.GET.get('employee')
        review_filter = self.request.GET.get('review')
        if year_filter:
            try:
                year_filter = int(year_filter)
                queryset = queryset.filter(created_date__year=year_filter)
            except ValueError:
                pass
        if employee_filter:
            queryset = queryset.filter(employee_id=employee_filter)
        if review_filter:
            queryset = queryset.filter(total_review=int(review_filter))
        return queryset

    def test_func(self) -> bool | None:
        return hasattr(self.request.user, "manager")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['years'] = Review.objects.dates('created_date', 'year')
        context['employees'] = Employee.objects.all()
        context['reviews'] = Review.SCORE_CHOICES
        context['selected_year'] = self.request.GET.get('year', '')
        context['selected_employee'] = self.request.GET.get('employee', '')
        context['selected_review'] = self.request.GET.get('review', '')
        return context
    
    def department_reviews(request):
        year_filter = request.GET.get('year')
        reviews = Review.objects.all()
        if year_filter:
            reviews = reviews.filter(created_date__year=year_filter)
        years = Review.objects.dates('created_date', 'year')
        context = {'department_reviews': reviews, 'years': years}
        return render(request, 'department_reviews.html', context)
    

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


class ReviewListView(generic.ListView):
    model = Review
    template_name = 'goals_management/review_list.html'
    context_object_name = 'review_list'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        return qs.filter(employee__user=user)
    

class GoalJournalDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Goal
    template_name = 'goals_management/goal_detail.html'
    form_class = GoalJournalForm
    
    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['goal'] = self.get_object()
        initial['owner'] = self.request.user
        return initial 

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form: Any) -> HttpResponse:
        form.instance.goal = self.get_object()
        form.instance.owner = self.request.user
        form.save()
        messages.success(self.request, _('Goal journal added!'))
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('goal_detail', kwargs={'pk':self.get_object().pk})
    

def goal_status_chart(request):
    def generate_chart():
        goals = Goal.objects.filter(owner=request.user)
        #priority graph
        priority_counts = goals.values('priority').annotate(count=models.Count('priority'))
        priority_labels = [dict(Goal.PRIORITY_CHOICES)[priority_count['priority']][2:] for priority_count in priority_counts]
        priority_values = [priority_count['count'] for priority_count in priority_counts]
        sns.set(style="whitegrid")
        plt.figure(figsize=(5, 4))
        ax2 = sns.barplot(x=priority_labels, y=priority_values, palette='dark:#5A9_r')
        ax2.set(xlabel='Priority')
        ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        plt.title('Goals by Priority')
        plt.tight_layout()
        for i, v in enumerate(priority_values):
            ax2.text(i, v, str(v), ha='center', va='bottom', color='black')
        tmpfile_priority_graph = 'goals_management/static/css/graphs/priority_graph.png'
        plt.savefig(tmpfile_priority_graph, format='png')
        plt.close()

        #status graph
        status_counts = goals.values('status').annotate(count=models.Count('status'))
        status_labels = [dict(Goal.GOAL_STATUS)[status_count['status']][2:] for status_count in status_counts]
        status_values = [status_count['count'] for status_count in status_counts]
        plt.figure(figsize=(5, 4))
        ax = plt.subplot()
        palette = sns.color_palette("BrBG", len(status_values)) 
        ax.pie(status_values, labels=status_labels, colors=palette, autopct='%1.0f%%', startangle=90)
        ax.axis('equal')
        plt.title('Goal Distribution by Status')
        plt.tight_layout()
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        tmpfile_status_graph = 'goals_management/static/css/graphs/status_graph.png'
        plt.savefig(tmpfile_status_graph, format='png')
        plt.close()

        #progress graph
        in_progress_goals = goals.filter(status=1)
        on_hold_goals = goals.filter(status=3)
        in_progress_progress_sum = in_progress_goals.aggregate(progress_sum=models.Sum('progress'))['progress_sum']
        on_hold_progress_sum = on_hold_goals.aggregate(progress_sum=models.Sum('progress'))['progress_sum']
        total_in_progress_goals = in_progress_goals.count()
        total_on_hold_goals = on_hold_goals.count()
        in_progress_progress_avg = in_progress_progress_sum / total_in_progress_goals if total_in_progress_goals > 0 else 0
        on_hold_progress_avg = on_hold_progress_sum / total_on_hold_goals if total_on_hold_goals > 0 else 0

        status_labels = ['In progress', 'On hold']
        progress_percentages = [in_progress_progress_avg, on_hold_progress_avg]
        plt.figure(figsize=(5, 2))
        ax = sns.barplot(x=progress_percentages, y=status_labels, palette='dark:#5A9_r')
        ax.set(xlabel='Progress (%)', ylabel='Status')
        plt.title('Average Goal Progress')
        plt.subplots_adjust(left=0.3, bottom=0.3)
        for i, v in enumerate(progress_percentages):
            ax.text(v + 0.02, i, f'{int(v * 100)}%', ha='left', va='center', color='white')
        tmpfile_progress_graph = 'goals_management/static/css/graphs/progress_graph.png'
        plt.savefig(tmpfile_progress_graph, format='png')
        plt.close()

    threading.Thread(target=generate_chart).start()
    total_goals = Goal.objects.filter(owner=request.user).count()
    context = {
        'priority_graph_path': 'static/css/graphs/priority_graph.png',
        'status_graph_path': 'static/css/graphs/status_graph.png',
        'progress_graph_path': 'static/css/graphs/progress_graph.png',
        'total_goals': total_goals,
    }
    return render(request, 'goals_management/statistics.html', context)
