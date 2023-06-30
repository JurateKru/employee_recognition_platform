from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ismart/', views.ismart, name='ismart'),
    path('goal-list/', views.GoalListView.as_view(), name='goal_list'),
    path('employees-list/', views.DepartmentEmployeesListView.as_view(), name='employees_list'),
    path('employees-list/detail/<int:pk>', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('employees-list/detail/create-review/', views.ReviewCreateView.as_view(), name='create_review'),
    path('goal-list/my-goal/<int:pk>', views.GoalDetailView.as_view(), name='goal_detail'),
    path('goal-list/my-goal/<int:pk>/update', views.GoalUpdateView.as_view(), name='update_goal'),
    path('goal-list/my-goal/<int:pk>/delete', views.GoalDeleteView.as_view(), name='goal_delete'),
    path('create-goal/', views.GoalCreateView.as_view(), name='create_goal'),
    
] 