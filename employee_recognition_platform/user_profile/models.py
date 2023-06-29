from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image
from goals_management.models import Employee, Manager


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(), 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name='profile',
        null=True, blank=True,
    )
    picture = models.ImageField(_("picture"), upload_to='user_profile/pictures', null=True, blank=True,)
    employee = models.OneToOneField(
        Employee,
        verbose_name=_("employee profile"), 
        on_delete=models.CASCADE,
        related_name='employee_profile',
        editable=False,
        null=True, blank=True,
    )
    # @property
    # def manager(self):
    #     if self.employee:
    #         return self.employee.manager
    #     return None

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if self.picture:
            pic = Image.open(self.picture.path)
            if pic.width > 300 or pic.height > 300:
                new_size = (300, 300)
                pic.thumbnail(new_size)
                pic.save(self.picture.path)
   
    
class ManagerProfile(models.Model):
    user = models.OneToOneField(
        get_user_model(), 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name='manager_user_profile',
        null=True, blank=True,
    )
    picture = models.ImageField(_("picture"), upload_to='user_profile/pictures', null=True, blank=True,)
    manager = models.OneToOneField(
        Manager,
        verbose_name=_("manager profile"), 
        on_delete=models.CASCADE,
        related_name='manager_profile',
        null=True, blank=True,
    )
    # @property
    # def employees(self):
    #     if self.manager:
    #         employees = Employee.objects.filter(manager=self.manager).all()
    #         return employees
    #     return None

    class Meta:
        verbose_name = _("manager profile")
        verbose_name_plural = _("manager profiles")

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if self.picture:
            pic = Image.open(self.picture.path)
            if pic.width > 300 or pic.height > 300:
                new_size = (300, 300)
                pic.thumbnail(new_size)
                pic.save(self.picture.path)

