from django.db import models

PART_TYPE_CHOICES = [
    ('Wing', 'Wing'),
    ('Fuselage', 'Fuselage'),
    ('Tail', 'Tail'),
    ('Avionics', 'Avionics'),
    ('Assembly', 'Assembly')
]

class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    responsible_part_type = models.CharField(
        max_length=50, 
        choices=PART_TYPE_CHOICES, 
        unique=True
    )
    def __str__(self):
        return f"{self.name} - {self.responsible_part_type}"
