from rest_framework import serializers
from .models import Aircraft

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['id', 'model', 'wing', 'fuselage', 'tail', 'avionics', 'assembled_at']
        read_only_fields = ['wing', 'fuselage', 'tail', 'avionics', 'assembled_at']

class AssembleAircraftSerializer(serializers.Serializer):
    model = serializers.ChoiceField(choices=['TB2', 'TB3', 'AKINCI', 'KIZILELMA'])
