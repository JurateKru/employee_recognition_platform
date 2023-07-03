from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ismart/', views.ismart, name='ismart'),
    path('goal-list/', views.GoalListView.as_view(), name='goal_list'),
    path('employees-list/', views.DepartmentEmployeesListView.as_view(), name='employees_list'),
    path('employees-list/detail/<int:pk>', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('employees-list/detail/<int:pk>/goals/', views.DepartmentGoalsListView.as_view(), name='employee_goals_list'),
    path('employees-list/detail/<int:pk>/create-review/', views.ReviewCreateView.as_view(), name='create_review'),
    path('goal-list/my-goal/<int:pk>', views.GoalDetailView.as_view(), name='goal_detail'),
    path('goal-list/my-goal/<int:pk>/update', views.GoalUpdateView.as_view(), name='update_goal'),
    path('goal-list/my-goal/<int:pk>/delete', views.GoalDeleteView.as_view(), name='delete_goal'),
    path('create-goal/', views.GoalCreateView.as_view(), name='create_goal'),
    path('department-reviews', views.DepartmentReviewsListView.as_view(), name='department_reviews'),
    path('department-reviews/detail/<int:pk>', views.ReviewDetailView.as_view(), name='review_detail'),
    path('department-reviews/detail/<int:pk>/update', views.ReviewUpdateView.as_view(), name='update_review'),
    path('department-reviews/detail/<int:pk>/delete', views.ReviewDeleteView.as_view(), name='delete_review'),
]