from rest_framework import serializers
from .models import SpyCat, Mission, Target
import requests


class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = ['id', 'name', 'years_of_experience', 'breed', 'salary']
        read_only_fields = ['id']

    _breeds_cache = None

    def validate_breed(self, value):
        if not SpyCatSerializer._breeds_cache:
            response = requests.get('https://api.thecatapi.com/v1/breeds')
            if response.status_code != 200:
                raise serializers.ValidationError("Failed to validate breed with TheCatAPI.")
            SpyCatSerializer._breeds_cache = [breed['name'] for breed in response.json()]

        if value not in SpyCatSerializer._breeds_cache:
            raise serializers.ValidationError(f"Invalid breed '{value}'.")
        return value


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'is_complete']
        read_only_fields = ['id', 'is_complete']

    def validate(self, attrs):
        if self.instance:
            if self.instance.is_complete:
                raise serializers.ValidationError("Cannot modify a completed target.")
            if self.instance.mission.is_complete:
                raise serializers.ValidationError("Cannot modify a target within a completed mission.")
        return attrs


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ['id', 'cat', 'is_complete', 'targets']
        read_only_fields = ['id', 'is_complete']

    def validate_targets(self, value):
        if not (1 <= len(value) <= 3):
            raise serializers.ValidationError("A mission must have between 1 and 3 targets.")
        return value

    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        targets = [Target(mission=mission, **target_data) for target_data in targets_data]
        Target.objects.bulk_create(targets)
        return mission

    def update(self, instance, validated_data):
        if instance.is_complete:
            raise serializers.ValidationError("Cannot modify a completed mission.")

        targets_data = validated_data.pop('targets', None)
        if targets_data:
            raise serializers.ValidationError("Updating targets through mission update is not supported.")

        return super().update(instance, validated_data)
