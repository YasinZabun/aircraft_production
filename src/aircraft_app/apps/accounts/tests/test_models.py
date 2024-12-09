from django.test import TestCase
from django.contrib.auth.models import User
from aircraft_app.apps.accounts.models import Profile
from aircraft_app.apps.teams.models import Team

class ProfileModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="WingTeam", responsible_part_type="Wing")

        self.user = User.objects.create_user(username="testuser", password="testpass")

        self.profile = Profile.objects.create(user=self.user, team=self.team)

    def test_profile_creation(self):
        """Test that a Profile instance is created correctly."""
        self.assertEqual(self.profile.user.username, "testuser")
        self.assertEqual(self.profile.team.name, "WingTeam")

    def test_profile_team_set_to_null_on_team_deletion(self):
        """Test that the team is set to null when the associated team is deleted."""
        self.team.delete()
        self.profile.refresh_from_db()
        self.assertIsNone(self.profile.team)

    def test_string_representation(self):
        """Test the string representation of the Profile model."""
        self.assertEqual(str(self.profile), f"{self.user.username} - {self.team.name}")
