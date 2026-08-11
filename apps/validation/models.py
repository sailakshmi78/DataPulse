from django.db import models
from apps.datasets_app.models import Dataset


class ValidationRun(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name='validation_runs'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    quality_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    total_checks = models.PositiveIntegerField(default=0)

    passed_checks = models.PositiveIntegerField(default=0)

    failed_checks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Validation #{self.id} - {self.dataset.original_filename}"


class DataIssue(models.Model):
    ISSUE_TYPES = [
        ('missing', 'Missing Value'),
        ('duplicate', 'Duplicate Value'),
        ('invalid', 'Invalid Value'),
        ('format', 'Invalid Format'),
        ('range', 'Out of Range'),
    ]

    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    validation_run = models.ForeignKey(
        ValidationRun,
        on_delete=models.CASCADE,
        related_name='issues'
    )

    column_name = models.CharField(max_length=255)

    row_number = models.PositiveBigIntegerField()

    issue_type = models.CharField(
        max_length=20,
        choices=ISSUE_TYPES
    )

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='medium'
    )

    value = models.TextField(
        null=True,
        blank=True
    )

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Row {self.row_number} - {self.column_name} - {self.issue_type}"
class ValidationRule(models.Model):
    CATEGORY_CHOICES = [
        ('completeness', 'Completeness'),
        ('uniqueness', 'Uniqueness'),
        ('validity', 'Validity'),
        ('format', 'Format'),
        ('consistency', 'Consistency'),
        ('range', 'Range'),
    ]

    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    RULE_TYPE_CHOICES = [
        ('missing', 'Missing Value'),
        ('duplicate', 'Duplicate'),
        ('range', 'Range'),
        ('format', 'Format'),
        ('invalid', 'Invalid Value'),
    ]

    code = models.CharField(
        max_length=100,
        unique=True
    )

    name = models.CharField(
        max_length=255
    )

    description = models.TextField()

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    rule_type = models.CharField(
    max_length=30,
    choices=RULE_TYPE_CHOICES,
    null=True,
    blank=True
    )
    
    column_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    parameters = models.JSONField(
        default=dict,
        blank=True
    )

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='medium'
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name