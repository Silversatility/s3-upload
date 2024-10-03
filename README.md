# S3 Upload with Encryption Using Django Rest Framework

This project demonstrates how to upload files to **AWS S3** with encryption using **Django Rest Framework (DRF)**. Files are encrypted before uploading to S3, and file metadata (such as file name and S3 URL) is stored in the database. This setup helps ensure that sensitive data is kept secure.

## Features

- **File Upload to S3**: Upload files to AWS S3 securely using `boto3`.
- **Encryption**: Files are encrypted using the `cryptography` library before being uploaded.
- **Metadata Storage**: File metadata (such as file name and URL) is stored in a database for easy retrieval.
- **List and Retrieve Files**: An API endpoint lists all files in the S3 bucket with file metadata.
- **Push Protection**: Ensure that sensitive information such as AWS credentials is not committed to the repository.

---

## Setup

### Prerequisites

- **Python 3.11**
- **Django 5.1**
- An **AWS account** with an S3 bucket created
- **boto3** for AWS interactions
- **cryptography** for file encryption
- **Django Rest Framework** for building APIs

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/s3-upload.git
    cd s3-upload
    ```

2. **Set Up a Virtual Environment**:
    (Optional, but recommended to avoid dependency conflicts)
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**:
    Install all required Python packages using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up AWS Credentials**:
    Create a `.env` file in the root directory of your project with the following content, replacing the placeholders with your AWS credentials:
    ```bash
    AWS_ACCESS_KEY_ID=your-access-key-id
    AWS_SECRET_ACCESS_KEY=your-secret-access-key
    AWS_STORAGE_BUCKET_NAME=your-bucket-name
    AWS_S3_REGION_NAME=your-region-name  # e.g., 'us-east-1'
    AWS_S3_CUSTOM_DOMAIN=your-bucket-name.s3.amazonaws.com
    ```

5. **Run Migrations**:
    Apply the migrations to set up the database schema for file storage:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Run the Django Server**:
    Start the development server:
    ```bash
    python manage.py runserver
    ```

---

## API Endpoints

### 1. **File Upload Endpoint**

- **URL**: `/api/upload/`
- **Method**: `POST`
- **Description**: Uploads an encrypted file to AWS S3 and stores its metadata (file name and URL) in the database.

#### Request (using Postman or cURL)
- **Content-Type**: `multipart/form-data`
- **Body**: Form-data with the key `file` containing the file to upload.

#### Example cURL Request:
```bash
curl -X POST http://127.0.0.1:8000/api/upload/ -F "file=@/path/to/your/file"



Technologies Used
Python 3.11
Django 5.1
Django Rest Framework
AWS S3 (via boto3)
cryptography for encryption
