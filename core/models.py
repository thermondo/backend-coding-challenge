from django.utils.translation import gettext_lazy as _

from django.db import models


class BaseModel(models.Model):
    created_date = models.DateField(verbose_name=_("Created At"), auto_now=True)
    modified_date = models.DateField(verbose_name=_("Updated At"), auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-pk"]
