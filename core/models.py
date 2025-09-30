import uuid
from django.db import models
from django.contrib.auth.models import User

class Household(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    country = models.CharField(max_length=2)
    city = models.CharField(max_length=80, blank=True)
    address = models.CharField(max_length=180, blank=True)
    timezone = models.CharField(max_length=64, default="America/Lima")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class HouseholdUser(models.Model):
    ROLE_CHOICES = (
        ("owner", "Owner"),
        ("viewer", "Viewer"),
    )
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="households")
    role = models.CharField(max_length=12, choices=ROLE_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("household", "user")
        ordering = ["-joined_at"]

    def __str__(self):
        return f"{self.user.username} @ {self.household.name} ({self.role})"