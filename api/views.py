from rest_framework import viewsets, permissions
from .serializers import DeviceSer, ReadingSer, AlertSer, GoalSer, HouseholdSer
from devices.models import Device, Reading
from alerts.models import Alert
from goals.models import Goal
from core.models import Household

class HouseholdViewSet(viewsets.ModelViewSet):
    queryset = Household.objects.all()
    serializer_class = HouseholdSer
    permission_classes = [permissions.AllowAny]

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSer
    permission_classes = [permissions.AllowAny]

class ReadingViewSet(viewsets.ModelViewSet):
    queryset = Reading.objects.all().order_by("-ts")
    serializer_class = ReadingSer
    permission_classes = [permissions.AllowAny]

class AlertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Alert.objects.all().order_by("-detected_at")
    serializer_class = AlertSer
    permission_classes = [permissions.AllowAny]

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSer
    permission_classes = [permissions.AllowAny]