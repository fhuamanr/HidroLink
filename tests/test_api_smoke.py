# tests/test_api_smoke.py
import uuid
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Household
from devices.models import Device, Reading
from datetime import datetime, timezone

def auth_headers(client):
    user = User.objects.create_user("tester", password="pass1234")
    resp = client.post("/api/token/", {"username": "tester", "password": "pass1234"})
    token = resp.json()["access"]
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}

def test_readings_list_smoke(client, db):
    h = Household.objects.create(id=uuid.uuid4(), name="Casa", country="PE")
    d = Device.objects.create(id=uuid.uuid4(), household=h, serial_number="SN-1", model="HL", fw_version="1.0")
    Reading.objects.create(device=d, ts=datetime.now(timezone.utc), volume_liters_delta=0.2)

    headers = auth_headers(client)
    r = client.get("/api/readings/", **headers)
    assert r.status_code == 200
    assert len(r.json()) >= 1

def test_daily_by_household(client, db):
    h = Household.objects.create(id=uuid.uuid4(), name="Casa", country="PE")
    d = Device.objects.create(id=uuid.uuid4(), household=h, serial_number="SN-2", model="HL", fw_version="1.0")
    Reading.objects.create(device=d, ts=datetime.now(timezone.utc), volume_liters_delta=0.3)

    headers = auth_headers(client)
    r = client.get("/api/readings/daily-by-household/", **headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)