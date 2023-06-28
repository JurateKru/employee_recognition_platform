from django.contrib import admin
from . import models


admin.site.register(models.Manager)
admin.site.register(models.Employee)
admin.site.register(models.Goal)
