from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE


class ExpenseInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, null=True)
    name = models.CharField(max_length=25)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=25)

    def __str__(self):
        return self.name