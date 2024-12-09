from django.contrib.auth.models import User
from django.db import models
from aircraft_app.apps.teams.models import Team

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"{self.user.username} - {self.team.name}"