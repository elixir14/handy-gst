from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class HandyBase(models.Model):
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(
        _("Updated Date"), auto_now_add=False, auto_now=True)
    # user = models.ForeignKey(User)

    class Meta:
        abstract = True