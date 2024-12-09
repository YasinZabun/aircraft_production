from django.test import TestCase
from aircraft_app.apps.teams.models import Team
from aircraft_app.apps.teams.serializers import TeamSerializer

class TeamSerializerTest(TestCase):
    def setUp(self):
        # Create sample data
        self.team_data = {
            "name": "TestTeam",
            "responsible_part_type": "Wing"
        }
        self.team = Team.objects.create(**self.team_data)

    def test_team_serializer_serialization(self):
        """Test that TeamSerializer correctly serializes a Team instance."""
        serializer = TeamSerializer(self.team)
        expected_data = {
            "id": self.team.id,
            "name": self.team.name,
            "responsible_part_type": self.team.responsible_part_type,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_team_serializer_deserialization_valid_data(self):
        """Test that TeamSerializer correctly deserializes valid data."""
        unique_team_data = {
            "name": "UniqueTestTeam",
            "responsible_part_type": "Fuselage"  # Assuming 'Fuselage' is a valid choice
        }
        serializer = TeamSerializer(data=unique_team_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)  # Print errors if invalid
        team = serializer.save()
        self.assertEqual(team.name, unique_team_data["name"])
        self.assertEqual(team.responsible_part_type, unique_team_data["responsible_part_type"])



    def test_team_serializer_deserialization_invalid_responsible_part_type(self):
        """Test that TeamSerializer raises a validation error for invalid responsible_part_type."""
        invalid_data = {
            "name": "InvalidTeam",
            "responsible_part_type": "InvalidPart"
        }
        serializer = TeamSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("responsible_part_type", serializer.errors)
        self.assertEqual(
            serializer.errors["responsible_part_type"][0].code, "invalid_choice"
        )

    def test_team_serializer_deserialization_missing_name(self):
        """Test that TeamSerializer raises a validation error for missing name."""
        incomplete_data = {
            "responsible_part_type": "Wing"
        }
        serializer = TeamSerializer(data=incomplete_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertEqual(
            serializer.errors["name"][0].code, "required"
        )

    def test_string_representation(self):
        """Test the string representation of the Team model."""
        self.assertEqual(
            str(self.team), 
            f"{self.team.name} - {self.team.responsible_part_type}"
        )
