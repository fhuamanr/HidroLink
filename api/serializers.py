from rest_framework import serializers
from devices.models import Device, Reading
from alerts.models import Alert
from goals.models import Goal
from core.models import Household
from billing.models import Tariff, HouseholdTariff

class HouseholdSer(serializers.ModelSerializer):
    class Meta:
        model = Household
        fields = "__all__"

class DeviceSer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"

class ReadingSer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = "__all__"

class AlertSer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = "__all__"

class GoalSer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = "__all__"

class TariffSer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = "__all__"

class HouseholdTariffSer(serializers.ModelSerializer):
    class Meta:
        model = HouseholdTariff
        fields = "__all__"