from django.core.management.base import BaseCommand
from core.models import Household
from devices.models import Device, Reading
from datetime import datetime, timedelta, timezone
import uuid, random
from billing.models import Tariff, HouseholdTariff

class Command(BaseCommand):
    help = "Crea datos de ejemplo"

    def handle(self, *args, **kwargs):
        h = Household.objects.create(id=uuid.uuid4(), name="Casa Miraflores2", country="PE", city="Lima")
        d = Device.objects.create(id=uuid.uuid4(), household=h, serial_number="SN-0002", model="HL-ESP33", fw_version="1.0.0")
        now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
        for i in range(96):  # 24h a cada 15 min
            ts = now - timedelta(minutes=15*i)
            Reading.objects.get_or_create(device=d, ts=ts, defaults={"volume_liters_delta": round(random.uniform(0.05, 0.4), 3)})
        self.stdout.write(self.style.SUCCESS("Seed listo"))
    # crear tarifa y asignarla al hogar demo
try:
    t, _ = Tariff.objects.get_or_create(
        name="Residencial Lima 2026",
        defaults=dict(currency="PEN", unit_price="0.005000", fixed_fee="10.00", effective_from="2025-01-01"),
    )
    HouseholdTariff.objects.get_or_create(household=h, tariff=t, assigned_from="2025-01-01")
except Exception as e:
    print("Seed tarifa error:", e)