from rest_framework import serializers
from .models import UploadedFile


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = "__all__"
