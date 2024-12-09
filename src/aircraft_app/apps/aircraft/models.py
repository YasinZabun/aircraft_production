from django.db import models
from aircraft_app.apps.parts.models import Part

AIRCRAFT_CHOICES = [
    ('TB2', 'TB2'),
    ('TB3', 'TB3'),
    ('AKINCI', 'AKINCI'),
    ('KIZILELMA', 'KIZILELMA')
]

class Aircraft(models.Model):
    model = models.CharField(max_length=50, choices=AIRCRAFT_CHOICES)
    wing = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='used_wing', null=True)
    fuselage = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='used_fuselage', null=True)
    tail = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='used_tail', null=True)
    avionics = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='used_avionics', null=True)
    assembled_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.model} - Assembled on {self.assembled_at.strftime('%Y-%m-%d %H:%M:%S')}"