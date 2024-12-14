from rest_framework import viewsets, permissions
from .models import Part
from .serializers import PartSerializer
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from aircraft_app.apps.parts.models import Part
from aircraft_app.apps.parts.serializers import PartSerializer
from aircraft_app.apps.common.permissions import IsAuthenticatedAndInTeam, IsTeamResponsibleForPart
class PartViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    ViewSet for managing parts by each team.
    Only the team's responsible part can be created.
    Deletion is allowed only if the part belongs to the user's team.
    """
    serializer_class = PartSerializer
    permission_classes = [IsAuthenticatedAndInTeam, IsTeamResponsibleForPart]

    def get_queryset(self):
        # Return only parts for the user's team
        user_team = self.request.user.profile.team
        return Part.objects.filter(team=user_team)

    def perform_destroy(self, instance):
        # "recycle" means delete
        # Allowed only if the part belongs to user's team (checked by permission)
        instance.delete()