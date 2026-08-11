from django.urls import path

from .views import upload_dataset, dataset_summary_api


urlpatterns = [
    path(
        "upload/",
        upload_dataset,
        name="upload_dataset"
    ),

    path(
        "<int:dataset_id>/",
        dataset_summary_api,
        name="dataset_summary_api"
    ),
]