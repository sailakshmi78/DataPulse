from django.contrib import admin
from django.urls import include, path
from .views import home

urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "api/datasets/",
        include("apps.datasets_app.urls")
    ),

    path(
        "api/datasets/",
        include("apps.validation.urls")
    ),

    path(
        "",
        home,
        name="home"
    ),
]