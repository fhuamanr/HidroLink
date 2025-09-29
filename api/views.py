from rest_framework import viewsets, permissions
from .serializers import DeviceSer, ReadingSer, AlertSer, GoalSer, HouseholdSer
from devices.models import Device, Reading
from alerts.models import Alert
from goals.models import Goal
from core.models import Household
from django.db.models import Sum
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models.functions import TruncDay

class HouseholdViewSet(viewsets.ModelViewSet):
    queryset = Household.objects.all()
    serializer_class = HouseholdSer
    permission_classes = [permissions.AllowAny]

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSer
    permission_classes = [permissions.AllowAny]


class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSer
    permission_classes = [permissions.AllowAny]


class ReadingViewSet(viewsets.ModelViewSet):
    queryset = Reading.objects.all().select_related("device__household").order_by("-ts")
    serializer_class = ReadingSer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="daily-by-household")
    def daily_by_household(self, request):
        # opcional: ?household=<uuid>|<nombre>&from=YYYY-MM-DD&to=YYYY-MM-DD
        qs = self.get_queryset()
        h = request.query_params.get("household")
        dt_from = request.query_params.get("from")
        dt_to = request.query_params.get("to")

        if h:
            qs = qs.filter(device__household__id=h) | qs.filter(device__household__name=h)
        if dt_from:
            qs = qs.filter(ts__date__gte=dt_from)
        if dt_to:
            qs = qs.filter(ts__date__lt=dt_to)

        agg = (qs
               .annotate(day=TruncDay("ts"))
               .values("device__household__name", "day")
               .annotate(liters=Sum("volume_liters_delta"))
               .order_by("day", "device__household__name"))
        return Response(list(agg))

class AlertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Alert.objects.select_related("device__household").order_by("-detected_at")
    serializer_class = AlertSer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="open")
    def open_alerts(self, request):
        qs = self.get_queryset().filter(resolved_at__isnull=True)
        data = qs.values("device__household__name", "type", "severity", "detected_at", "message")
        return Response(list(data))