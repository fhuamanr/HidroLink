from locust import HttpUser, task, between
import json, os

BASE = os.getenv("BASE_URL", "http://127.0.0.1:8000")
USER = os.getenv("TEST_USER", "tester")
PASS = os.getenv("TEST_PASS", "pass1234")

class ApiUser(HttpUser):
    wait_time = between(0.5, 1.5)
    token = None

    def on_start(self):
        # obtener JWT
        r = self.client.post(f"{BASE}/api/token/",
                             headers={"Content-Type":"application/json"},
                             data=json.dumps({"username": USER, "password": PASS}))
        r.raise_for_status()
        self.token = r.json()["access"]

    def auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def readings_list(self):
        self.client.get(f"{BASE}/api/readings/", headers=self.auth_headers(), name="GET /api/readings/")

    @task(1)
    def readings_cost(self):
        # usa el primer household por nombre
        h = self.client.get(f"{BASE}/api/households/", headers=self.auth_headers(),
                            name="GET /api/households/")
        if h.ok and h.json():
            name = h.json()[0]["name"]
            self.client.get(f"{BASE}/api/readings/cost/?household={name}",
                            headers=self.auth_headers(), name="GET /api/readings/cost")