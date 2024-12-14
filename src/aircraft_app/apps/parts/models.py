# parts/models.py
from django.db import models
from aircraft_app.apps.teams.models import Team

AIRCRAFT_CHOICES = [
    ('TB2', 'TB2'),
    ('TB3', 'TB3'),
    ('AKINCI', 'AKINCI'),
    ('KIZILELMA', 'KIZILELMA')
]

PART_TYPE_CHOICES = [
    ('Wing', 'Wing'),
    ('Fuselage', 'Fuselage'),
    ('Tail', 'Tail'),
    ('Avionics', 'Avionics'),
]

class Part(models.Model):
    part_type = models.CharField(max_length=50, choices=PART_TYPE_CHOICES)
    aircraft_model = models.CharField(max_length=50, choices=AIRCRAFT_CHOICES)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    # Additional fields if needed (serial number, etc.)
    def __str__(self):
        return f"{self.part_type} - {self.aircraft_model} - {self.stock} - {self.team}"
    
