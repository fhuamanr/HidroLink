import uuid
import pytest
from core.models import Household
from devices.models import Device, Reading
from django.db import IntegrityError
from datetime import datetime, timezone

@pytest.mark.django_db
def test_device_unique_serial():
    h = Household.objects.create(id=uuid.uuid4(), name="Casa", country="PE")
    Device.objects.create(id=uuid.uuid4(), household=h, serial_number="SN-1", model="HL", fw_version="1.0")
    with pytest.raises(IntegrityError):
        Device.objects.create(id=uuid.uuid4(), household=h, serial_number="SN-1", model="HL", fw_version="1.0")

@pytest.mark.django_db
def test_reading_pk_compuesta_idempotencia():
    h = Household.objects.create(id=uuid.uuid4(), name="Casa", country="PE")
    d = Device.objects.create(id=uuid.uuid4(), household=h, serial_number="SN-2", model="HL", fw_version="1.0")
    ts = datetime.now(timezone.utc).replace(microsecond=0)
    Reading.objects.create(device=d, ts=ts, volume_liters_delta=0.2)
    with pytest.raises(IntegrityError):
        Reading.objects.create(device=d, ts=ts, volume_liters_delta=0.3)