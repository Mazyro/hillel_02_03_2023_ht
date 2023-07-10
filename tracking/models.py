from django.db import models

from project.mixins.models import PKMixin


# Create your models here.


class Tracking(PKMixin):
    method = models.CharField(max_length=12)
    url = models.CharField(max_length=255)
    data = models.JSONField(default=dict)
