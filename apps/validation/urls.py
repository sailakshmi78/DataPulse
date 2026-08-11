from django.urls import path

from .views import (
    validate_dataset_api,
    validation_results_api,
)


urlpatterns = [
    path(
        "<int:dataset_id>/validate/",
        validate_dataset_api,
        name="validate_dataset_api"
    ),

    path(
        "<int:dataset_id>/validation/",
        validation_results_api,
        name="validation_results_api"
    ),
]