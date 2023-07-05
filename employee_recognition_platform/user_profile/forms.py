from django.contrib.auth import get_user_model
from django import forms
from . import models


User = get_user_model()


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ()


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ("picture",)


class ManagerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = models.ManagerProfile
        fields = ("picture",)
