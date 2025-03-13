from django.urls import path

from django_ckeditors.views import (
    process_unused_image_urls,
    upload_image,
)

urlpatterns = [
    path(
        "image_upload/",
        upload_image,
        name="ck_editors_upload_image",
    ),
    path(
        "unused_image_url/",
        process_unused_image_urls,
        name="ck_editors_unused_image_url",
    ),
]
