import os

import boto3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cryptography.fernet import Fernet
from .models import UploadedFile
from .serializers import FileUploadSerializer
from botocore.exceptions import NoCredentialsError
from .serializers import UploadedFileSerializer

key = Fernet.generate_key()
cipher = Fernet(key)


class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']

            file_content = file.read()
            encrypted_content = cipher.encrypt(file_content)

            s3 = boto3.client(
                's3',
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_S3_REGION_NAME"),
            )

            file_key = f'encrypted_{file.name}'

            try:

                s3.put_object(
                    Bucket=os.getenv("AWS_STORAGE_BUCKET_NAME"),
                    Key=file_key,
                    Body=encrypted_content,
                    ContentType=file.content_type
                )

                uploaded_file = UploadedFile.objects.create(
                    file_path=f"https://{os.getenv('AWS_S3_CUSTOM_DOMAIN')}/{file_key}",
                    original_file_name=file.name
                )

                return Response(
                    {
                        "message": "File uploaded and encrypted successfully",
                        "file_key": file_key,
                        "s3_url": f'https://{os.getenv("AWS_S3_CUSTOM_DOMAIN")}/{file_key}',
                        "db_id": uploaded_file.id,
                    },
                    status=status.HTTP_201_CREATED,
                )

            except NoCredentialsError:
                return Response({
                    'error': 'AWS credentials not available'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileListView(APIView):
    def get(self, request):
        try:

            s3 = boto3.client(
                "s3",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_S3_REGION_NAME",)
            )

            s3_objects = s3.list_objects_v2(Bucket=os.getenv("AWS_STORAGE_BUCKET_NAME"))

            if "Contents" in s3_objects:

                files = [
                    {
                        "file_name": obj["Key"],
                        "s3_url": f"https://{os.getenv('AWS_S3_CUSTOM_DOMAIN')}/{obj['Key']}",
                        "last_modified": obj["LastModified"].strftime("%Y-%m-%d %H:%M:%S"),
                        "size": obj["Size"],
                    }
                    for obj in s3_objects["Contents"]
                ]

                return Response(files, status=200)
            else:
                return Response(
                    {"message": "No files found in the S3 bucket."}, status=404
                )

        except NoCredentialsError:
            return Response({"error": "AWS credentials not available"}, status=500)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
