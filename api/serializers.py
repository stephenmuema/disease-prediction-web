from rest_framework import serializers

from api.models import Files


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'
