from django.test import TestCase
from aircraft_app.apps.parts.models import Part
from aircraft_app.apps.teams.models import Team

class PartModelTest(TestCase):
    def setUp(self):
        # Create a team
        self.team = Team.objects.create(name="WingTeam", responsible_part_type="Wing")

        # Create a part
        self.part = Part.objects.create(
            part_type="Wing",
            aircraft_model="TB2",
            stock=10,
            team=self.team
        )

    def test_part_creation(self):
        """Test that a Part instance is created correctly."""
        self.assertEqual(self.part.part_type, "Wing")
        self.assertEqual(self.part.aircraft_model, "TB2")
        self.assertEqual(self.part.stock, 10)
        self.assertEqual(self.part.team, self.team)

    def test_string_representation(self):
        """Test the string representation of the Part model."""
        self.assertEqual(
            str(self.part), 
            f"{self.part.part_type} - {self.part.aircraft_model} - {self.part.stock} - {self.part.team}"
        )
