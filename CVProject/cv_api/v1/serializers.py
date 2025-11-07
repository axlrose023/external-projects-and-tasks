from rest_framework import serializers
from cv_app.models import CV

class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = ["id", "firstname", "lastname", "bio", "skills", "projects", "contacts"]
        read_only_fields = ["id"]

    def validate_skills(self, value):
        if value in (None, ""):
            return []
        if not isinstance(value, (list, tuple)) or not all(isinstance(x, str) for x in value):
            raise serializers.ValidationError("skills must be a list of strings.")
        return list(value)

    def validate_projects(self, value):
        if value in (None, ""):
            return []
        if not isinstance(value, (list, tuple)) or not all(isinstance(x, dict) for x in value):
            raise serializers.ValidationError("projects must be a list of objects.")
        return list(value)

    def validate_contacts(self, value):
        if value in (None, ""):
            return {}
        if not isinstance(value, dict):
            raise serializers.ValidationError("contacts must be an object.")
        return value
