# devices/models.py
from django.db import models
from django.contrib.postgres.fields import JSONField
from core.models import Household

class Device(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    household = models.ForeignKey(Household, on_delete=models.RESTRICT, related_name="devices")
    serial_number = models.CharField(max_length=64, unique=True)
    model = models.CharField(max_length=60)
    fw_version = models.CharField(max_length=30)
    install_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=16, default="active")
    device_capabilities = JSONField(default=dict)
    last_seen_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.serial_number}"

class Reading(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="readings")
    ts = models.DateTimeField()
    flow_lpm = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    pressure_kpa = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    volume_liters_delta = models.DecimalField(max_digits=12, decimal_places=4)
    temp_c = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)

    class Meta:
        unique_together = ("device", "ts")
        indexes = [
            models.Index(fields=["device", "-ts"], name="idx_readings_device_ts_desc"),
        ]

    def __str__(self):
        return f"{self.device_id}@{self.ts}"