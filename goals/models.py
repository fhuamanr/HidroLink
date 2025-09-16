from django.db import models
from core.models import Household
from django.conf import settings

class Goal(models.Model):
    WEEK = "week"; MONTH = "month"
    PERIODS = [(WEEK, "Week"), (MONTH, "Month")]

    id = models.BigAutoField(primary_key=True)
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name="goals")
    period = models.CharField(max_length=10, choices=PERIODS)
    target_liters = models.DecimalField(max_digits=14, decimal_places=3)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=16, default="active")

    class Meta:
        ordering = ["-start_date"]