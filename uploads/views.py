import logging

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from cryptography.fernet import Fernet
from .models import UploadedFile


key = Fernet.generate_key()
cipher = Fernet(key)


logger = logging.getLogger(__name__)


@csrf_exempt  # Disable CSRF for testing
def upload_file(request):
    if request.method == "POST":
        # Log the request for debugging
        print(f"Request HEADERS: {request.headers}")
        print(f"Request FILES: {request.FILES}")
        print(f"Request POST: {request.POST}")

        file = request.FILES.get("file")

        if file:
            # Read and encrypt the file content
            file_content = file.read()
            encrypted_content = cipher.encrypt(file_content)

            # Save the encrypted file
            file_key = f"encrypted_{file.name}"
            path = default_storage.save(file_key, ContentFile(encrypted_content))

            # Save the file metadata in the database
            uploaded_file = UploadedFile.objects.create(
                file_path=path, original_file_name=file.name
            )

            # Return success response
            return JsonResponse(
                {
                    "message": "File uploaded and encrypted successfully",
                    "file_key": path,
                    "db_id": uploaded_file.id,  # Return the database ID of the saved record
                },
                status=201,
            )

    return JsonResponse({"error": "File upload failed"}, status=400)
