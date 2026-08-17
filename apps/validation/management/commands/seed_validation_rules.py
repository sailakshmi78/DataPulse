from django.core.management.base import BaseCommand
from apps.validation.models import ValidationRule


class Command(BaseCommand):
    help = "Create default DataPulse validation rules"

    def handle(self, *args, **kwargs):

        rules = [
            {
                "code": "MISSING_VALUES",
                "name": "Missing Values Check",
                "description": "Detect missing values in dataset",
                "category": "completeness",
                "rule_type": "missing",
                "column_name": None,
                "parameters": {},
                "severity": "high",
                "is_active": True,
            },
            {
                "code": "DUPLICATE_VALUES",
                "name": "Duplicate Values Check",
                "description": "Detect duplicate records in dataset",
                "category": "uniqueness",
                "rule_type": "duplicate",
                "column_name": None,
                "parameters": {},
                "severity": "high",
                "is_active": True,
            },
        ]

        for rule_data in rules:

            rule, created = ValidationRule.objects.update_or_create(
                code=rule_data["code"],
                defaults=rule_data,
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created rule: {rule.code}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Rule already exists: {rule.code}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Default validation rules ready."
            )
        )