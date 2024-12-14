from rest_framework.test import APITestCase
from rest_framework import status
from aircraft_app.apps.parts.models import Part
from aircraft_app.apps.teams.models import Team
from aircraft_app.apps.accounts.models import Profile
from django.contrib.auth.models import User

class PartViewSetTest(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.team = Team.objects.create(name="WingTeam", responsible_part_type="Wing")
        self.profile = Profile.objects.create(user=self.user, team=self.team)
        self.client.login(username="testuser", password="testpass")

        # Create a part
        self.part = Part.objects.create(part_type="Wing", aircraft_model="TB2", stock=10, team=self.team)

    def test_list_parts(self):
        """Test listing parts for the authenticated user's team."""
        response = self.client.get("/api/parts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Parse response JSON
        response_data = response.json()

        # Check if the data matches
        self.assertEqual(len(response_data), 1)  # Ensure one part is listed
        self.assertEqual(response_data[0]["part_type"], "Wing")
        self.assertEqual(response_data[0]["aircraft_model"], "TB2")

    def test_create_part(self):
        """Test creating a new part."""
        data = {
            "part_type": "Wing",
            "aircraft_model": "TB3",
            "stock": 5,
        }
        response = self.client.post("/api/parts/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the part is created
        self.assertEqual(Part.objects.count(), 2)
        new_part = Part.objects.get(aircraft_model="TB3")
        self.assertEqual(new_part.stock, 5)

    def test_recycle_part(self):
        """Test deleting (recycling) a part."""
        response = self.client.delete(f"/api/parts/{self.part.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the part is deleted
        self.assertEqual(Part.objects.count(), 0)
