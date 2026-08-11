from django.contrib.auth.models import User
from django.core.files import File

from apps.datasets_app.models import Dataset
from apps.validation.models import ValidationRun, DataIssue

from services.validation_service import validate_dataset


# Actual test CSV on disk
file_path = "datasets/sample/validation_test.csv"


# Get or create test user
user, created = User.objects.get_or_create(
    username="testuser"
)


# Remove previous test records
Dataset.objects.filter(
    original_filename="validation_test.csv"
).delete()


# Open the real CSV file and attach it to Django FileField
with open(file_path, "rb") as csv_file:

    dataset = Dataset.objects.create(
        owner=user,
        original_filename="validation_test.csv",
        file=File(
            csv_file,
            name="validation_test.csv"
        ),
        file_type="csv",
        file_size=0,
        row_count=4,
        column_count=2,
        status="uploaded"
    )


# Run validation
validation_run = validate_dataset(dataset)


print("Validation service completed!")

print()
print("Validation Run ID:", validation_run.id)
print("Status:", validation_run.status)
print("Total checks:", validation_run.total_checks)
print("Passed checks:", validation_run.passed_checks)
print("Failed checks:", validation_run.failed_checks)
print("Quality score:", validation_run.quality_score)

print()
print("Data Issues:")

for issue in DataIssue.objects.filter(
    validation_run=validation_run
):
    print(
        issue.issue_type,
        "|",
        issue.column_name,
        "| Row:",
        issue.row_number,
        "|",
        issue.message
    )