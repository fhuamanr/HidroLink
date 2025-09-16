from django.db import models

class Household(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=120)
    country = models.CharField(max_length=60)
    region = models.CharField(max_length=60, blank=True)
    city = models.CharField(max_length=60, blank=True)
    address = models.CharField(max_length=255, blank=True)
    timezone = models.CharField(max_length=60, default="America/Lima")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class HouseholdUser(models.Model):
    OWNER = "owner"
    VIEWER = "viewer"
    ROLES = [(OWNER, "Owner"), (VIEWER, "Viewer")]

    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES, default=VIEWER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("household", "user")