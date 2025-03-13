"""django-ckeditors models"""

from django.db import models
from django.utils.translation import pgettext_lazy as _


class UnusedImageURLS(models.Model):
    """Image urls that are no longer referenced in a ckEditor"""

    image_url = models.URLField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_(
            "Verbose name",
            "Image URL",
        ),
        help_text=_(
            "Help text",
            "The images url.",
        ),
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Verbose name", "Created"),
        help_text=_("Help text", "The date and time when this record was created."),
    )

    deleted = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Verbose name", "Deleted"),
        help_text=_(
            "Help text",
            "The date and time when this record was deleted (if applicable).",
        ),
    )

    class Meta:
        verbose_name = _(
            "Verbose name",
            "Django CKE Unused Images",
        )
        verbose_name_plural = _(
            "Verbose name",
            "Django CKE Unused Images",
        )
        app_label = "django_ckeditors"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "image_url",
                ],
                name="djcke_image_url_no_duplicates",
                violation_error_message="Django CKeditor removed image url may not be duplicated.",
            )
        ]

    def __str__(self):
        return str(self.image_url)
