import boto3
from botocore.exceptions import NoCredentialsError
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from myproject.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_S3_REGION_NAME,
    AWS_STORAGE_BUCKET_NAME
)

def upload_file_to_s3(file, file_name):
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_S3_REGION_NAME
    )

    try:
        s3.upload_fileobj(file, AWS_STORAGE_BUCKET_NAME, file_name)
        return f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/{file_name}"
    except NoCredentialsError:
        print("Brak danych uwierzytelniających do S3")
        return None


class Article(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            img = img.convert("RGB")

            # Konwersja do WebP
            output = BytesIO()
            img.save(output, format='WEBP', quality=80)
            output.seek(0)

            # Generowanie poprawnej nazwy pliku
            filename = os.path.basename(self.image.name)
            new_filename = f"articles/{os.path.splitext(filename)[0]}.webp"

            # Zapis pliku na Amazon S3
            uploaded_url = upload_file_to_s3(output, new_filename)
            if uploaded_url:
                self.image.name = new_filename  # Przechowuj ścieżkę do pliku w bazie danych

        super().save(*args, **kwargs)