from django.test import TestCase
from django.contrib.auth.models import User
from aircraft_app.apps.accounts.models import Profile
from aircraft_app.apps.teams.models import Team
from aircraft_app.apps.accounts.serializers import AccountSerializer

class AccountSerializerTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="WingTeam", responsible_part_type="Wing")

        self.user = User.objects.create_user(username="testuser", password="testpass")

        self.profile = Profile.objects.create(user=self.user, team=self.team)

    def test_serializer_with_valid_data(self):
        """Test serialization of a valid Profile instance."""
        serializer = AccountSerializer(instance=self.profile)
        data = serializer.data

        self.assertEqual(data["id"], self.profile.id)
        self.assertEqual(data["user"], self.user.id)
        self.assertEqual(data["team"], self.team.id)

    def test_serializer_with_invalid_data(self):
        """Test validation with invalid data."""
        invalid_data = {
            "user": -58,  # 58 is Sivas
            "team": -58,  # 58 is Sivas
        }
        serializer = AccountSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)
        self.assertIn("team", serializer.errors)

    def test_serializer_create(self):
        """Test serializer's create method."""
        new_user = User.objects.create_user(username="newuser", password="newpass")

        data = {
            "user": new_user.id,
            "team": self.team.id,
        }
        serializer = AccountSerializer(data=data)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)
        profile = serializer.save()

        self.assertEqual(profile.user, new_user)
        self.assertEqual(profile.team, self.team)


    def test_serializer_update(self):
        """Test serializer's update method."""
        new_team = Team.objects.create(name="NewTeam", responsible_part_type="Avionics")
        data = {
            "team": new_team.id,
        }
        serializer = AccountSerializer(instance=self.profile, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_profile = serializer.save()

        self.assertEqual(updated_profile.team, new_team)
