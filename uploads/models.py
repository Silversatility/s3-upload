from django.db import models


class UploadedFile(models.Model):
    file_path = models.CharField(max_length=255)
    original_file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)