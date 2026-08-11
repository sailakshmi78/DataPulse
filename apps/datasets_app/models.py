from django.db import models
from django.contrib.auth.models import User


class Dataset(models.Model):
    STATUS_CHOICES = [
        ('uploaded', 'Uploaded'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='datasets'
    )

    original_filename = models.CharField(max_length=255)

    file = models.FileField(upload_to='datasets/')

    file_type = models.CharField(max_length=20)

    file_size = models.BigIntegerField()

    row_count = models.PositiveBigIntegerField(default=0)

    column_count = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='uploaded'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.original_filename


class DatasetColumn(models.Model):
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name='columns'
    )

    name = models.CharField(max_length=255)

    data_type = models.CharField(max_length=50)

    null_count = models.PositiveBigIntegerField(default=0)

    unique_count = models.PositiveBigIntegerField(default=0)

    duplicate_count = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.dataset.original_filename} - {self.name}"