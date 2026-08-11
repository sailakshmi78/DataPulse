from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from apps.datasets_app.models import Dataset

from services.validation_service import validate_dataset


@csrf_exempt
def validate_dataset_api(request, dataset_id):
    """
    Run validation for a specific dataset.
    """

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "message": "Only POST requests are allowed."
            },
            status=405
        )

    try:
        dataset = Dataset.objects.get(id=dataset_id)

    except Dataset.DoesNotExist:
        return JsonResponse(
            {
                "success": False,
                "message": "Dataset not found."
            },
            status=404
        )

    try:
        validation_run = validate_dataset(dataset)

        return JsonResponse(
            {
                "success": True,
                "message": "Dataset validation completed.",
                "validation": {
                    "id": validation_run.id,
                    "dataset_id": dataset.id,
                    "status": validation_run.status,
                    "total_checks": validation_run.total_checks,
                    "passed_checks": validation_run.passed_checks,
                    "failed_checks": validation_run.failed_checks,
                    "quality_score": (
                        float(validation_run.quality_score)
                        if validation_run.quality_score is not None
                        else None
                    ),
                }
            },
            status=200
        )

    except Exception as error:
        return JsonResponse(
            {
                "success": False,
                "message": "Dataset validation failed.",
                "error": str(error)
            },
            status=500
        )
def validation_results_api(request, dataset_id):
    """
    Return the latest validation results for a dataset.
    """

    if request.method != "GET":
        return JsonResponse(
            {
                "success": False,
                "message": "Only GET requests are allowed."
            },
            status=405
        )

    try:
        dataset = Dataset.objects.get(id=dataset_id)

    except Dataset.DoesNotExist:
        return JsonResponse(
            {
                "success": False,
                "message": "Dataset not found."
            },
            status=404
        )

    validation_run = (
        dataset.validation_runs
        .order_by("-id")
        .first()
    )

    if not validation_run:
        return JsonResponse(
            {
                "success": False,
                "message": "No validation run found for this dataset."
            },
            status=404
        )

    issues = validation_run.issues.all().order_by("row_number")

    issue_data = []

    for issue in issues:
        issue_data.append(
            {
                "id": issue.id,
                "issue_type": issue.issue_type,
                "severity": issue.severity,
                "column_name": issue.column_name,
                "row_number": issue.row_number,
                "value": issue.value,
                "message": issue.message,
            }
        )

    return JsonResponse(
        {
            "success": True,
            "dataset": {
                "id": dataset.id,
                "filename": dataset.original_filename,
            },
            "validation": {
                "id": validation_run.id,
                "status": validation_run.status,
                "total_checks": validation_run.total_checks,
                "passed_checks": validation_run.passed_checks,
                "failed_checks": validation_run.failed_checks,
                "quality_score": (
                    float(validation_run.quality_score)
                    if validation_run.quality_score is not None
                    else None
                ),
                "issues": issue_data,
            },
        },
        status=200
    )