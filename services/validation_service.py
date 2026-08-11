from django.utils import timezone

from apps.datasets_app.models import Dataset
from apps.validation.models import ValidationRun, DataIssue

from data_engine.reader import read_dataset
from services.validation_engine import run_validation


def validate_dataset(dataset):
    """
    Run DataPulse validation for a Dataset and save
    the results into the database.
    """

    validation_run = ValidationRun.objects.create(
        dataset=dataset,
        status="running",
        started_at=timezone.now()
    )

    try:
        dataframe = read_dataset(dataset.file.path)

        results = run_validation(dataframe)

        total_checks = 0
        failed_checks = 0

        # =========================================================
        # DUPLICATE ISSUES
        # =========================================================

        for issue in results["duplicates"]:
            total_checks += 1
            failed_checks += 1

            DataIssue.objects.create(
                validation_run=validation_run,
                column_name=", ".join(issue["columns"]),
                row_number=issue["row_number"],
                issue_type="duplicate",
                severity="medium",
                value=str(issue["values"]),
                message="Duplicate record detected."
            )

        # =========================================================
        # MISSING-VALUE ISSUES
        # =========================================================

        for issue in results["missing_values"]:
            total_checks += issue["missing_count"]
            failed_checks += issue["missing_count"]

            for row_number in issue["rows"]:
                DataIssue.objects.create(
                    validation_run=validation_run,
                    column_name=issue["column_name"],
                    row_number=row_number,
                    issue_type="missing",
                    severity="high",
                    value=None,
                    message="Missing value detected."
                )

        # =========================================================
        # RANGE ISSUES
        # =========================================================

        for issue in results["range_issues"]:
            total_checks += 1
            failed_checks += 1

            DataIssue.objects.create(
                validation_run=validation_run,
                column_name=issue["column_name"],
                row_number=issue["row_number"],
                issue_type="range",
                severity="high",
                value=str(issue["value"]),
                message=(
                    f"Value must be between "
                    f"{issue['minimum']} and {issue['maximum']}."
                )
            )

        # =========================================================
        # FORMAT ISSUES
        # =========================================================

        for issue in results["format_issues"]:
            total_checks += 1
            failed_checks += 1

            DataIssue.objects.create(
                validation_run=validation_run,
                column_name=issue["column_name"],
                row_number=issue["row_number"],
                issue_type="format",
                severity="high",
                value=str(issue["value"]),
                message=issue["message"]
            )

        # =========================================================
        # REAL DATASET QUALITY SCORE
        # =========================================================

        dataset_rows = len(dataframe)

        failed_checks = (
            len(results["duplicates"])
            + sum(
                issue["missing_count"]
                for issue in results["missing_values"]
            )
            + len(results["range_issues"])
            + len(results["format_issues"])
        )

        total_checks = dataset_rows

        passed_checks = max(
            total_checks - failed_checks,
            0
        )

        if total_checks > 0:
            quality_score = (
                passed_checks / total_checks
            ) * 100
        else:
            quality_score = 100

        # =========================================================
        # SAVE VALIDATION RUN
        # =========================================================

        validation_run.total_checks = total_checks
        validation_run.passed_checks = passed_checks
        validation_run.failed_checks = failed_checks
        validation_run.quality_score = quality_score
        validation_run.status = "completed"
        validation_run.completed_at = timezone.now()

        validation_run.save()

        # =========================================================
        # UPDATE DATASET STATUS
        # =========================================================

        dataset.status = "completed"

        dataset.save(
            update_fields=[
                "status",
                "updated_at"
            ]
        )

        return validation_run

    except Exception:
        validation_run.status = "failed"
        validation_run.completed_at = timezone.now()

        validation_run.save(
            update_fields=[
                "status",
                "completed_at"
            ]
        )

        dataset.status = "failed"

        dataset.save(
            update_fields=[
                "status",
                "updated_at"
            ]
        )

        raise