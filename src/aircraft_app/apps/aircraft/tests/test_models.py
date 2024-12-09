from django.test import TestCase
from aircraft_app.apps.aircraft.models import Aircraft, AIRCRAFT_CHOICES
from aircraft_app.apps.parts.models import Part
from aircraft_app.apps.teams.models import Team
from django.core.exceptions import ValidationError

class AircraftModelTest(TestCase):
    def setUp(self):
        self.wing_team = Team.objects.create(name="WingTeam", responsible_part_type="Wing")
        self.fuselage_team = Team.objects.create(name="FuselageTeam", responsible_part_type="Fuselage")
        self.tail_team = Team.objects.create(name="TailTeam", responsible_part_type="Tail")
        self.avionics_team = Team.objects.create(name="AvionicsTeam", responsible_part_type="Avionics")

        self.wing = Part.objects.create(part_type="Wing", aircraft_model="TB2", stock=1, team=self.wing_team)
        self.fuselage = Part.objects.create(part_type="Fuselage", aircraft_model="TB2", stock=1, team=self.fuselage_team)
        self.tail = Part.objects.create(part_type="Tail", aircraft_model="TB2", stock=1, team=self.tail_team)
        self.avionics = Part.objects.create(part_type="Avionics", aircraft_model="TB2", stock=1, team=self.avionics_team)

        self.aircraft = Aircraft.objects.create(
            model="TB2",
            wing=self.wing,
            fuselage=self.fuselage,
            tail=self.tail,
            avionics=self.avionics,
        )

    def test_aircraft_creation(self):
        """Test that an Aircraft instance is created correctly."""
        self.assertEqual(self.aircraft.model, "TB2")
        self.assertEqual(self.aircraft.wing, self.wing)
        self.assertEqual(self.aircraft.fuselage, self.fuselage)
        self.assertEqual(self.aircraft.tail, self.tail)
        self.assertEqual(self.aircraft.avionics, self.avionics)
        self.assertIsNotNone(self.aircraft.assembled_at)

    def test_aircraft_model_choices(self):
        """Test that the model field only allows valid choices."""
        aircraft = Aircraft(
            model="INVALID",
            wing=self.wing,
            fuselage=self.fuselage,
            tail=self.tail,
            avionics=self.avionics,
        )
        with self.assertRaises(ValidationError) as context:
            aircraft.full_clean()

        self.assertIn("Value 'INVALID' is not a valid choice", str(context.exception))
        self.assertIn("model", context.exception.message_dict)
        self.assertIn("Value 'INVALID' is not a valid choice", context.exception.message_dict["model"][0])


    def test_aircraft_str_representation(self):
        """Test the string representation of the Aircraft model."""
        self.assertEqual(str(self.aircraft), f"{self.aircraft.model} - Assembled on {self.aircraft.assembled_at.strftime('%Y-%m-%d %H:%M:%S')}")

    def test_part_deletion_cascade(self):
        """Test that deleting a part also deletes the associated Aircraft."""
        self.wing.delete()
        with self.assertRaises(Aircraft.DoesNotExist):
            self.aircraft.refresh_from_db()

    def test_null_part_fields(self):
        """Test creating an Aircraft with missing parts."""
        aircraft_without_fuselage = Aircraft.objects.create(
            model="TB2",
            wing=self.wing,
            tail=self.tail,
            avionics=self.avionics,
        )
        self.assertIsNone(aircraft_without_fuselage.fuselage)
