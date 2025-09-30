import uuid
from datetime import datetime, timezone
from django.contrib.auth.models import User
from core.models import Household
from devices.models import Device, Reading
from billing.models import Tariff, HouseholdTariff

def auth_headers(client):
    User.objects.filter(username="tester").delete()
    u = User.objects.create_user("tester", password="pass1234")
    resp = client.post("/api/token/", {"username": "tester", "password": "pass1234"})
    assert resp.status_code == 200, resp.content
    return {"HTTP_AUTHORIZATION": f"Bearer {resp.json()['access']}"}

def test_cost_ok(client, db):
    h = Household.objects.create(id=uuid.uuid4(), name="Casa Miraflores", country="PE")
    d = Device.objects.create(id=uuid.uuid4(), household=h, serial_number="SN-9", model="HL", fw_version="1.0")
    Reading.objects.create(device=d, ts=datetime.now(timezone.utc), volume_liters_delta=1.5)

    t = Tariff.objects.create(name="Residencial Lima 2025", currency="PEN", unit_price="0.005", fixed_fee="10.00", effective_from="2025-01-01")
    HouseholdTariff.objects.create(household=h, tariff=t, assigned_from="2025-01-01")

    headers = auth_headers(client)
    r = client.get("/api/readings/cost/?household=Casa%20Miraflores&from=2025-01-01&to=2030-01-01", **headers)
    assert r.status_code == 200
    data = r.json()
    assert data["currency"] == "PEN"
    assert data["estimated_cost"] >= 10.00  # al menos tarifa fija