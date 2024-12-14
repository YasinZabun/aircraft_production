from django.test import TestCase
from aircraft_app.apps.parts.serializers import PartSerializer
from aircraft_app.apps.parts.models import Part
from aircraft_app.apps.teams.models import Team

class PartSerializerTest(TestCase):
    def setUp(self):
        # Create a team and a part
        self.team = Team.objects.create(name="WingTeam", responsible_part_type="Wing")
        self.part = Part.objects.create(part_type="Wing", aircraft_model="TB2", stock=10, team=self.team)

    def test_serializer_with_valid_data(self):
        """Test serialization of a valid Part instance."""
        serializer = PartSerializer(instance=self.part)
        data = serializer.data

        self.assertEqual(data["part_type"], "Wing")
        self.assertEqual(data["aircraft_model"], "TB2")
        self.assertEqual(data["stock"], 10)

    def test_serializer_with_invalid_data(self):
        """Test validation of invalid serializer data."""
        invalid_data = {
            "part_type": "InvalidPartType",
            "aircraft_model": "TB2",
            "stock": 10,
            "team": None,
        }
        serializer = PartSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("part_type", serializer.errors)
