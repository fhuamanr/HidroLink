from django.db import models
from core.models import Household

class Tariff(models.Model):
    name = models.CharField(max_length=120, unique=True)
    currency = models.CharField(max_length=8, default="PEN")
    unit_price = models.DecimalField(max_digits=12, decimal_places=6)  # por litro
    fixed_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-effective_from"]

    def __str__(self):
        return f"{self.name} ({self.currency})"

class HouseholdTariff(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT)
    assigned_from = models.DateField()
    assigned_to = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("household", "assigned_from")
        ordering = ["-assigned_from"]