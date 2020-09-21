from django.contrib import admin
from django.conf import settings
from django.urls import include, path, re_path


urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"api/", include("polls.urls")),
]
