"""django-ckeditors custom widget"""

from __future__ import annotations

import json
import logging

from django import forms, get_version
from django.conf import settings
from django.forms.renderers import get_default_renderer
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

if get_version() >= "4.0":
    from django.utils.translation import gettext_lazy as _
else:
    from django.utils.translation import (
        ugettext_lazy as _,  # [import-error]
    )

logger = logging.getLogger(__name__)


class CKEditorsWidget(forms.Widget):
    template_name = "django_ckeditors/widget.html"

    def __init__(
        self,
        attrs=None,
        data_extra: str | list[str] | dict[str, str] | None = None,
        toolbar_config: str = "default",
        admin_calling: bool = False,
    ):
        """
        A custom Django widget for integrating CKEditor 5 rich-text editor.

        Attributes:
           * template_name (str): The template used to render the widget.
           * data_extra (str | list[str] | dict[str, str] | None): Additional data
             to pass to the editor (optional).
           * admin_calling (bool): Indicates whether the widget is being used in
             the Django admin (default: False).
           * _config_errors (list): A list to store any errors encountered during
             configuration loading.
           * config (dict): The final configuration dictionary for the CKEditor
             instance.

        Methods:
            __init__(*attrs, admin_calling=False, data_extra=None, toolbar_config="default"):
                Initializes the widget, loads and validates the CKEditor configuration.

            render(name, value, attrs=None, renderer=None):
                Renders the CKEditor widget as HTML (see detailed documentation below).

        """
        self.data_extra = data_extra
        self.admin_calling = admin_calling

        self._config_errors: list = []
        self.config: dict = {}
        if toolbar_config not in settings.DJ_CKE_EDITORS_CONFIGS:
            toolbar_config = "default"

        try:
            configs = getattr(settings, "DJ_CKE_EDITORS_CONFIGS")
            try:
                self.config.update(configs[toolbar_config])
            except (TypeError, KeyError, ValueError) as ex:
                self._config_errors.append(self.format_error(ex))
                logger.exception("django-ckeditor config error")
        except AttributeError as ex:
            self._config_errors.append(self.format_error(ex))

        default_attrs = {"class": "django_ckeditors"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def format_error(self, ex):
        return "{} {}".format(
            _("Check the correct settings.DJ_CKE_EDITORS_CONFIGS "),
            str(ex),
        )

    class Media:
        css = {
            "all": [
                "django_ckeditors/dist/styles.css",
            ],
        }
        custom_css = getattr(settings, "DJ_CKE_CUSTOM_CSS", None)
        if custom_css:
            css["all"].append(custom_css)
        # TODO: Need to find a simple way to make this conditional
        # on admin_calling...
        # js = ["django_ckeditors/dist/bundle.js"]
        configs = getattr(settings, "DJ_CKE_EDITORS_CONFIGS", None)
        if configs is not None:
            for config in configs:
                language = configs[config].get("language")
                if language:
                    languages = []
                    if isinstance(language, dict) and language.get("ui"):
                        language = language.get("ui")
                    elif isinstance(language, str):
                        languages.append(language)
                    elif isinstance(language, list):
                        languages = language
                    for lang in languages:
                        if lang != "en":
                            js += [f"django_ckeditors/dist/translations/{lang}.js"]

    def render(self, name, value, attrs=None, renderer=None):
        """
        Renders the CKEditor widget as HTML.

        Args:
            name (str): The name of the form field.
            value (str): The initial value of the field.
            attrs (dict, optional): HTML attributes to be applied to the widget.
            renderer (object, optional): A Django template renderer instance.

        Returns:
            str: The rendered HTML for the CKEditor widget.

        Behavior:
            1. Retrieves the base context using `super().get_context()`.
            2. If `CKEDITORS_USER_LANGUAGE` setting is True, attempts to set
               the editor language to the user's current language.
            3. Gets the default renderer if not provided.
            4. Populates the context with configuration, script ID, upload URL,
               CSRF cookie name, and JSON-encoded extra data.
            5. Optionally includes configuration errors in the context (commented out).
            6. Renders the widget template using the prepared context.
        """
        context = super().get_context(name, value, attrs)
        use_language = getattr(settings, "CKEDITORS_USER_LANGUAGE", False)
        if use_language:
            language = get_language().lower()
            if language:
                self.config["language"] = language

        if renderer is None:
            renderer = get_default_renderer()

        context["config"] = self.config
        context["script_id"] = f'{attrs["id"]}_script'
        context["upload_image_url"] = reverse("ck_editors_upload_image")
        context["upload_unused_image_url"] = reverse("ck_editors_unused_image_url")
        context["csrf_cookie_name"] = settings.DJ_CKE_CSRF_COOKIE_NAME
        context["data_extra"] = json.dumps(self.data_extra)
        # .. NOTE: Config errors probably should not be sent to the end user.
        # if self._config_errors:
        #   context["errors"] = ErrorList(self._config_errors) #pylint:disable=commented-out code

        return mark_safe(renderer.render(self.template_name, context))
