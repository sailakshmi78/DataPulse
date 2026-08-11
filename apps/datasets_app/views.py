from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from .models import Dataset, DatasetColumn

from data_engine.reader import read_dataset
from data_engine.profiler import profile_dataset

@csrf_exempt
def upload_dataset(request):
    """
    Upload a CSV dataset, profile it,
    and save dataset metadata.
    """

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "message": "Only POST requests are allowed."
            },
            status=405
        )

    uploaded_file = request.FILES.get("file")

    if not uploaded_file:
        return JsonResponse(
            {
                "success": False,
                "message": "No file uploaded."
            },
            status=400
        )

    filename = uploaded_file.name

    if not filename.lower().endswith(".csv"):
        return JsonResponse(
            {
                "success": False,
                "message": "Only CSV files are supported."
            },
            status=400
        )

    user, created = User.objects.get_or_create(
        username="testuser"
    )

    dataset = Dataset.objects.create(
        owner=user,
        original_filename=filename,
        file=uploaded_file,
        file_type="csv",
        file_size=uploaded_file.size,
        status="processing"
    )

    try:
        dataframe = read_dataset(dataset.file.path)

        profile = profile_dataset(dataframe)

        dataset.row_count = profile["row_count"]
        dataset.column_count = profile["column_count"]
        dataset.status = "completed"

        dataset.save(
            update_fields=[
                "row_count",
                "column_count",
                "status",
                "updated_at"
            ]
        )

        for column_name, column_data in profile["columns"].items():

            DatasetColumn.objects.create(
                dataset=dataset,
                name=column_name,
                data_type=column_data["data_type"],
                null_count=column_data["missing_count"],
                unique_count=column_data["unique_count"],
                duplicate_count=column_data["duplicate_count"]
            )

        return JsonResponse(
            {
                "success": True,
                "message": "Dataset uploaded and profiled successfully.",
                "dataset": {
                    "id": dataset.id,
                    "filename": dataset.original_filename,
                    "file_type": dataset.file_type,
                    "file_size": dataset.file_size,
                    "rows": dataset.row_count,
                    "columns": dataset.column_count,
                    "status": dataset.status
                }
            },
            status=201
        )

    except Exception as error:

        dataset.status = "failed"

        dataset.save(
            update_fields=[
                "status",
                "updated_at"
            ]
        )

        return JsonResponse(
            {
                "success": False,
                "message": "Dataset processing failed.",
                "error": str(error)
            },
            status=500
        )
def dataset_summary_api(request, dataset_id):
    """
    Return summary information for a dataset.
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

    latest_validation = (
        dataset.validation_runs
        .order_by("-id")
        .first()
    )

    issue_count = 0
    validation_status = None
    quality_score = None

    if latest_validation:
        validation_status = latest_validation.status
        quality_score = (
            float(latest_validation.quality_score)
            if latest_validation.quality_score is not None
            else None
        )
        issue_count = latest_validation.issues.count()

    return JsonResponse(
        {
            "success": True,
            "dataset": {
                "id": dataset.id,
                "filename": dataset.original_filename,
                "file_type": dataset.file_type,
                "file_size": dataset.file_size,
                "rows": dataset.row_count,
                "columns": dataset.column_count,
                "status": dataset.status,
                "created_at": dataset.created_at,
                "updated_at": dataset.updated_at,
            },
            "validation": {
                "status": validation_status,
                "quality_score": quality_score,
                "issue_count": issue_count,
            },
        },
        status=200
    )