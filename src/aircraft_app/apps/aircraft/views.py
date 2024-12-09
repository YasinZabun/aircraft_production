from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from aircraft_app.apps.aircraft.models import Aircraft
from aircraft_app.apps.aircraft.serializers import AircraftSerializer,AssembleAircraftSerializer
from aircraft_app.apps.parts.models import Part
from aircraft_app.apps.common.permissions import (
    IsAuthenticatedAndInTeam,
    IsTeamResponsibleForPart,
    IsAssemblyTeam
)

class AircraftViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """
    View to list all produced aircraft.
    """
    serializer_class = AircraftSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Aircraft.objects.all()

@swagger_auto_schema(
    method='post',
    request_body=AssembleAircraftSerializer,
    responses={201: openapi.Response('Aircraft assembled successfully')}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAssemblyTeam])
def assemble_aircraft(request):
    """
    Assembly endpoint:
    POST with {"model": "TB2"} to assemble that aircraft.
    Checks if all required parts (Wing, Fuselage, Tail, Avionics) are available for that model.
    If not, returns an error.
    If yes, picks one of each (stock > 0), decrements stock, and creates an Aircraft.
    """
    serializer = AssembleAircraftSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    model = request.data.get('model')
    if model not in ['TB2', 'TB3', 'AKINCI', 'KIZILELMA']:
        return Response({"error": "Invalid aircraft model."}, status=status.HTTP_400_BAD_REQUEST)

    required_part_types = ['Wing', 'Fuselage', 'Tail', 'Avionics']
    parts_to_use = {}

    for p_type in required_part_types:
        # find a part with the correct model and stock > 0
        part = Part.objects.filter(
            part_type=p_type,
            aircraft_model=model,
            stock__gt=0
        ).first()
        if not part:
            # Missing this part
            return Response({"error": f"Missing {p_type} for {model}."}, status=status.HTTP_400_BAD_REQUEST)
        parts_to_use[p_type] = part

    # If we reach here, we have all parts.
    # Decrement stock and create the Aircraft
    for part in parts_to_use.values():
        part.stock -= 1
        part.save()

    aircraft = Aircraft.objects.create(
        model=model,
        wing=parts_to_use['Wing'],
        fuselage=parts_to_use['Fuselage'],
        tail=parts_to_use['Tail'],
        avionics=parts_to_use['Avionics']
    )

    serializer = AircraftSerializer(aircraft)
    return Response(serializer.data, status=status.HTTP_201_CREATED)