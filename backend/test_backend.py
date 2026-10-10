import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import app
from app.db.session import init_db

class TestAnnaSetuModularBackend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = TestClient(app)

    def test_01_health_check(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "healthy")

    def test_02_mandi_rates(self):
        res = self.client.get("/api/v1/mandi/rates")
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.json()), 4)

    def test_03_procurement_flow(self):
        payload = {
            "farmerName": "Kisan Balwant",
            "cropType": "Wheat (Lokwan)",
            "quantityQuintals": 80.0,
            "pricePerQuintal": 2350.0,
            "location": "Karnal, Haryana",
            "whatsappAlerts": True
        }
        res = self.client.post("/api/v1/procurement/listings", json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertTrue(data["id"].startswith("ORD-"))

        # Fetch orders
        orders_res = self.client.get("/api/v1/procurement/orders")
        self.assertEqual(orders_res.status_code, 200)
        self.assertTrue(any(o["id"] == data["id"] for o in orders_res.json()))

    def test_04_surplus_flow(self):
        payload = {
            "donorOrg": "Marriott Banquet",
            "category": "Cooked Meals (Veg)",
            "servings": 250,
            "pickupWindowHours": "Next 2.5 Hours",
            "locationZone": "North Sector 5"
        }
        post_res = self.client.post("/api/v1/surplus/donations", json=payload)
        self.assertEqual(post_res.status_code, 201)
        surplus_id = post_res.json()["id"]

        reserve_res = self.client.post(f"/api/v1/surplus/reserve/{surplus_id}", json={
            "ngoId": "Feeding Lives Foundation",
            "estimatedPickupTime": "Within 40 mins"
        })
        self.assertEqual(reserve_res.status_code, 200)

    def test_05_logistics_and_pass(self):
        match_res = self.client.post("/api/v1/logistics/smart-match", json={
            "cropType": "Wheat (Lokwan)",
            "quantity": 100.0,
            "originDistrict": "Karnal, Haryana"
        })
        self.assertEqual(match_res.status_code, 200)
        pass_id = match_res.json()["transitPassId"]

        pass_res = self.client.get(f"/api/v1/logistics/pass/{pass_id}")
        self.assertEqual(pass_res.status_code, 200)
        self.assertEqual(pass_res.json()["passId"], pass_id)

    def test_06_grievance_support(self):
        res = self.client.post("/api/v1/support/grievance", json={
            "name": "Kuldeep Singh",
            "category": "Weight Discrepancy",
            "issueDetails": "Discrepancy at Mandi weighbridge"
        })
        self.assertEqual(res.status_code, 201)
        self.assertTrue(res.json()["ticketId"].startswith("GRV-"))

    def test_07_analytics_stats(self):
        res = self.client.get("/api/v1/analytics/stats")
        self.assertEqual(res.status_code, 200)
        self.assertGreater(res.json()["connectedFarmers"], 10000)

    def test_08_auth_token_me(self):
        res = self.client.post("/api/v1/auth/login", json={
            "usernameOrEmail": "farmer_ramesh",
            "password": "Farmer@123"
        })
        self.assertEqual(res.status_code, 200)
        token = res.json()["accessToken"]

        me_res = self.client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(me_res.status_code, 200)
        self.assertEqual(me_res.json()["username"], "farmer_ramesh")

if __name__ == "__main__":
    unittest.main()
