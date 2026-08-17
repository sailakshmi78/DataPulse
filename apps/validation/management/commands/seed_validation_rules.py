from django.core.management.base import BaseCommand
from apps.validation.models import ValidationRule


class Command(BaseCommand):
    help = "Create and activate the default DataPulse validation rules"

    def handle(self, *args, **options):

        rules = [
            {
                "code": "MISSING_VALUES",
                "name": "Missing Values Check",
                "description": "Detect missing, null, empty, or whitespace-only values.",
                "category": "completeness",
                "rule_type": "missing",
                "column_name": None,
                "parameters": {},
                "severity": "high",
            },
            {
                "code": "DUPLICATE_VALUES",
                "name": "Duplicate Values Check",
                "description": "Detect duplicate records in the dataset.",
                "category": "uniqueness",
                "rule_type": "duplicate",
                "column_name": None,
                "parameters": {},
                "severity": "high",
            },
            {
                "code": "AGE_RANGE",
                "name": "Age Range Check",
                "description": "Validate age values within the configured range.",
                "category": "range",
                "rule_type": "range",
                "column_name": "age",
                "parameters": {
                    "minimum": 0,
                    "maximum": 120,
                },
                "severity": "high",
            },
            {
                "code": "EMAIL_FORMAT",
                "name": "Email Format Check",
                "description": "Validate email values against the configured email format.",
                "category": "format",
                "rule_type": "format",
                "column_name": "email",
                "parameters": {
                    "pattern": r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
                },
                "severity": "high",
            },
        ]

        # Disable the old duplicate/legacy rules.
        ValidationRule.objects.filter(
            code__in=["REQUIRED_VALUE", "UNIQUE_RECORD"]
        ).update(is_active=False)

        for rule_data in rules:

            code = rule_data["code"]

            rule, created = ValidationRule.objects.update_or_create(
                code=code,
                defaults={
                    **rule_data,
                    "is_active": True,
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created rule: {code}"
                    )
                )
            else:
                self.stdout.write(
                    f"Rule already exists/updated: {code}"
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Default DataPulse validation rules ready."
            )
        )