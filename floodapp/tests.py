from django.test import TestCase, Client
from django.urls import reverse
from datetime import date
from .models import FloodControl


class FloodControlTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = FloodControl.objects.create(
            description="Test Project",
            location="Butuan",
            contractor="ME 3 CONSTRUCTION",
            cost=1000000.0,
            completion_date=date(2025, 5, 30),
        )

    def test_health_endpoint(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy"})

    def test_get_floodcontrol_list(self):
        response = self.client.get(reverse("get_floodcontrol"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) >= 1)

    def test_create_floodcontrol(self):
        data = {
            "description": "New Flood Control",
            "location": "Agusan del Norte",
            "contractor": "RAMISES CONSTRUCTION",
            "cost": 5000000.0,
            "completion_date": "2025-05-30",
        }
        response = self.client.post(
            reverse("create_floodcontrol"), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["description"], "New Flood Control")

    def test_update_floodcontrol(self):
        url = reverse("update_floodcontrol", args=[self.project.id])
        response = self.client.put(
            url,
            {"description": "Updated Project"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["description"], "Updated Project")

    def test_delete_floodcontrol(self):
        url = reverse("delete_floodcontrol", args=[self.project.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Flood control project deleted"})
