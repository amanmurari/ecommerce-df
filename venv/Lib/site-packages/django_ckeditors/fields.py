"""django-ckeditors custom text field"""

from __future__ import annotations

from django.db import models

from .widgets import CKEditorsWidget


class CKEditorsField(models.TextField):
    def __init__(
        self,
        *args,
        data_extra: str | list[str] | dict[str, str] | None = None,
        toolbar_config: str = "default",
        **kwargs,
    ) -> None:
        self.data_extra = data_extra
        self.toolbar_config = toolbar_config
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        # Extract and analyze the provided widget
        admin_calling = False
        widget = kwargs.get("widget", None)
        # INFO: This is to let the widget know
        # that the js needs to be included for admin.
        if "django.contrib.admin.widgets" in str(widget):
            admin_calling = True

        # Define default values
        defaults = {
            "widget": CKEditorsWidget(
                admin_calling=admin_calling,
                data_extra=self.data_extra,
                toolbar_config=self.toolbar_config,
            ),
        }

        # Merge defaults with kwargs and pass to super().formfield
        return super().formfield(**{**defaults, **kwargs})
