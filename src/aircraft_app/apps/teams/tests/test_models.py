from django.core.exceptions import ValidationError
from django.test import TestCase
from aircraft_app.apps.teams.models import Team

class TeamModelTest(TestCase):
    def test_create_team_with_valid_data(self):
        """Test creating a team with valid data."""
        team = Team.objects.create(name="TestTeam", responsible_part_type="Wing")
        self.assertEqual(team.name, "TestTeam")
        self.assertEqual(team.responsible_part_type, "Wing")

    def test_create_team_with_duplicate_responsible_part_type(self):
        """Test that creating a team with a duplicate responsible_part_type raises an error."""
        Team.objects.create(name="Team1", responsible_part_type="Wing")
        with self.assertRaises(ValidationError):
            team = Team(name="Team2", responsible_part_type="Wing")
            team.full_clean()  # This validates the model and raises ValidationError for duplicate part types

    def test_create_team_with_invalid_responsible_part_type(self):
        """Test that creating a team with an invalid responsible_part_type raises an error."""
        with self.assertRaises(ValidationError):
            team = Team(name="InvalidTeam", responsible_part_type="InvalidPart")
            team.full_clean()
