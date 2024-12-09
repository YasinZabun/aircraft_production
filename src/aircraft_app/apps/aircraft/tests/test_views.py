from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from aircraft_app.apps.aircraft.models import Aircraft
from aircraft_app.apps.parts.models import Part
from aircraft_app.apps.teams.models import Team
from aircraft_app.apps.accounts.models import Profile



class AircraftViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.wing_team = Team.objects.create(name="WingTeam", responsible_part_type="Wing")
        self.user_profile = Profile.objects.create(user=self.user, team=self.wing_team)

        self.assembly_team = Team.objects.create(name="AssemblyTeam", responsible_part_type="Assembly")
        self.assembly_user = User.objects.create_user(username="assemblyuser", password="assemblypass")
        self.assembly_user_profile = Profile.objects.create(user=self.assembly_user, team=self.assembly_team)
        self.assembly_user.profile.save()

        self.client.login(username="testuser", password="testpass")

        self.wing = Part.objects.create(part_type="Wing", aircraft_model="TB2", stock=1, team=self.wing_team)
        self.fuselage = Part.objects.create(part_type="Fuselage", aircraft_model="TB2", stock=1, team=self.wing_team)
        self.tail = Part.objects.create(part_type="Tail", aircraft_model="TB2", stock=1, team=self.wing_team)
        self.avionics = Part.objects.create(part_type="Avionics", aircraft_model="TB2", stock=1, team=self.wing_team)

        self.aircraft = Aircraft.objects.create(
            model="TB2",
            wing=self.wing,
            fuselage=self.fuselage,
            tail=self.tail,
            avionics=self.avionics,
        )

    def test_list_aircraft(self):
        """Test listing all aircraft."""
        response = self.client.get("/api/aircraft/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["model"], "TB2")

    def test_assemble_aircraft_success(self):
        """Test successful aircraft assembly."""
        self.client.logout()
        self.client.login(username="assemblyuser", password="assemblypass")

        data = {"model": "TB2"}
        response = self.client.post("/api/assemble/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["model"], "TB2")
        self.assertEqual(Aircraft.objects.count(), 2)


        self.wing.refresh_from_db()
        self.assertEqual(self.wing.stock, 0)

    def test_assemble_aircraft_missing_part(self):
        """Test assembly fails due to a missing part."""
        self.client.logout()
        self.client.login(username="assemblyuser", password="assemblypass")


        self.wing.stock = 0
        self.wing.save()

        data = {"model": "TB2"}
        response = self.client.post("/api/assemble/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Missing Wing for TB2.", response.data["error"])

    def test_assemble_aircraft_invalid_model(self):
        """Test assembly fails due to an invalid aircraft model."""
        self.client.logout()
        self.client.login(username="assemblyuser", password="assemblypass")

        data = {"model": "INVALID_MODEL"}
        response = self.client.post("/api/assemble/", data)
        

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("model", response.data)
        self.assertIn("INVALID_MODEL", response.data["model"][0])
        self.assertIn("invalid_choice", response.data["model"][0].code)


    def test_unauthorized_access(self):
        """Test that unauthorized users cannot access the assembly endpoint."""
        self.client.logout()

        data = {"model": "TB2"}
        response = self.client.post("/api/assemble/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
