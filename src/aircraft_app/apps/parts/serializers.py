# parts/serializers.py
from rest_framework import serializers
from .models import Part

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ['id', 'part_type', 'aircraft_model', 'team', 'stock']
        extra_kwargs = {
            'team': {'required': False},  # Prevent team field from being required in the input
        }

    def validate(self, attrs):
        # Ensure that the user's team matches the part_type
        request = self.context['request']

        # Ensure the user has a team assigned
        user_team = getattr(request.user.profile, 'team', None)
        if not user_team:
            raise serializers.ValidationError("Your user does not belong to any team.")
        
        if attrs.get('part_type') != user_team.responsible_part_type:
            raise serializers.ValidationError("Your team is not responsible for this type of part.")
        # Also ensure that the team field is set to the user's team
        if 'team' in attrs and attrs['team'] != user_team:
            raise serializers.ValidationError("You cannot assign this part to a different team than your own.")
        return attrs

    def create(self, validated_data):
        # Force the team to the user’s team
        validated_data['team'] = self.context['request'].user.profile.team
        return super().create(validated_data)