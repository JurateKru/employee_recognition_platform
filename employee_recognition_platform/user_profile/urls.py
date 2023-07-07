from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.profile, name='profile'),
    path('<int:user_id>/', views.profile, name='profile_detail'),
    path('update/', views.profile_update, name='profile_update'),
    path('manager-update/', views.manager_profile_update, name='manager_profile'),
]
