from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ismart/', views.ismart, name='ismart'),
    path('create-goal/', views.GoalCreateView.as_view(), name='create_goal'),

]