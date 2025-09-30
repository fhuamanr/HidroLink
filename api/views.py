# api/views.py
from uuid import UUID
from decimal import Decimal

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.models import Sum
from django.db.models.functions import TruncDay, Coalesce

from .serializers import DeviceSer, ReadingSer, AlertSer, GoalSer, HouseholdSer
from devices.models import Device, Reading
from alerts.models import Alert
from goals.models import Goal
from core.models import Household
from billing.models import HouseholdTariff


class HouseholdViewSet(viewsets.ModelViewSet):
    queryset = Household.objects.all().order_by("name")
    serializer_class = HouseholdSer
    permission_classes = [permissions.IsAuthenticated]


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.select_related("household").all()
    serializer_class = DeviceSer
    permission_classes = [permissions.IsAuthenticated]


class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.select_related("household").all()
    serializer_class = GoalSer
    permission_classes = [permissions.IsAuthenticated]


class ReadingViewSet(viewsets.ModelViewSet):
    queryset = Reading.objects.select_related("device__household").all().order_by("-ts")
    serializer_class = ReadingSer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="daily-by-household")
    def daily_by_household(self, request):
        """
        Agregación de consumo diario por hogar.
        Parámetros opcionales: ?household=<uuid|nombre>&from=YYYY-MM-DD&to=YYYY-MM-DD
        """
        h = request.query_params.get("household")
        dt_from = request.query_params.get("from")
        dt_to = request.query_params.get("to")

        qs = self.get_queryset()
        # Filtrado por hogar (UUID o nombre, case-insensitive)
        if h:
            try:
                UUID(h)  # si es UUID válido
                qs = qs.filter(device__household__id=h)
            except (ValueError, TypeError):
                qs = qs.filter(device__household__name__iexact=h)

        if dt_from:
            qs = qs.filter(ts__date__gte=dt_from)
        if dt_to:
            qs = qs.filter(ts__date__lt=dt_to)

        agg = (
            qs.annotate(day=TruncDay("ts"))
              .values("device__household__name", "day")
              .annotate(liters=Coalesce(Sum("volume_liters_delta"), Decimal("0")))
              .order_by("day", "device__household__name")
        )

        data = [
            {
                "household": row["device__household__name"],
                "day": row["day"].isoformat() if hasattr(row["day"], "isoformat") else row["day"],
                "liters": float(row["liters"]),
            }
            for row in agg
        ]
        return Response(data)

    @action(detail=False, methods=["get"], url_path="cost")
    def cost(self, request):
        """
        Costo estimado = (suma de litros en el rango) * unit_price + fixed_fee
        Requiere que el hogar tenga una tarifa asignada (HouseholdTariff).
        Parámetros: ?household=<uuid|nombre>&from=YYYY-MM-DD&to=YYYY-MM-DD
        """
        h = request.query_params.get("household")  # uuid o nombre
        dt_from = request.query_params.get("from")
        dt_to = request.query_params.get("to")

        if not h:
            return Response({"detail": "faltó household"}, status=400)

        qs = self.get_queryset()

        # Resolver el household y filtrar por él (acepta UUID o nombre)
        household = None
        try:
            UUID(h)
            qs = qs.filter(device__household__id=h)
            household = Household.objects.filter(id=h).first()
        except (ValueError, TypeError):
            qs = qs.filter(device__household__name__iexact=h)
            household = Household.objects.filter(name__iexact=h).first()

        if dt_from:
            qs = qs.filter(ts__gte=dt_from)
        if dt_to:
            qs = qs.filter(ts__lt=dt_to)

        if not household:
            return Response({"detail": "household no encontrado"}, status=400)

        agg = qs.aggregate(liters=Coalesce(Sum("volume_liters_delta"), Decimal("0")))
        liters = Decimal(agg["liters"] or 0)

        # Tarifa vigente (última asignación)
        ht = HouseholdTariff.objects.filter(household=household).order_by("-assigned_from").first()
        if not ht:
            return Response({"detail": "hogar sin tarifa asignada"}, status=400)

        t = ht.tariff
        cost = liters * t.unit_price + t.fixed_fee

        # Redondeo a 2 decimales en la respuesta
        return Response({
            "household": household.name,
            "from": dt_from, "to": dt_to,
            "liters": float(liters),
            "unit_price": float(t.unit_price),
            "fixed_fee": float(t.fixed_fee),
            "currency": t.currency,
            "estimated_cost": float(Decimal(cost).quantize(Decimal("0.01")))
        })


class AlertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Alert.objects.select_related("device__household").all().order_by("-detected_at")
    serializer_class = AlertSer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="open")
    def open_alerts(self, request):
        qs = self.get_queryset().filter(resolved_at__isnull=True)
        data = list(qs.values("device__household__name", "type", "severity", "detected_at", "message"))
        return Response(data)