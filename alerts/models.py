from django.db import models
from django.conf import settings
from devices.models import Device

class Alert(models.Model):
    LEAK = "leak"
    SPIKE = "spike"
    OFFLINE = "offline"
    TYPES = [(LEAK, "Leak"), (SPIKE, "Spike"), (OFFLINE, "Offline")]

    LOW = "low"; MED = "medium"; HI = "high"
    SEV = [(LOW, "Low"), (MED, "Medium"), (HI, "High")]

    id = models.BigAutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="alerts")
    type = models.CharField(max_length=16, choices=TYPES)
    severity = models.CharField(max_length=16, choices=SEV)
    detected_at = models.DateTimeField()
    message = models.TextField(blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    extra = models.JSONField(default=dict)

    class Meta:
        indexes = [
            models.Index(fields=["device", "-detected_at"], name="idx_alerts_device_time"),
        ]