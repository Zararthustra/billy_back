from django.db import models
from django.conf import settings


class Summary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    year = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    sold = models.FloatField(default=0)


class Movement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    year = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    day = models.IntegerField(default=0)
    lib = models.CharField(max_length=200)
    value = models.FloatField(default=0)
    sold = models.FloatField(default=0)
    rec = models.BooleanField()
