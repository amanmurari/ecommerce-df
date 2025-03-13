"""django-ckeditors app.py file"""

from __future__ import annotations

from django.apps import AppConfig
from django.conf import settings


class DjangoCKEditorsConfig(AppConfig):
    name = "django_ckeditors"

    def ready(self):
        if not hasattr(settings, "DJ_CKE_BULK_CREATE_BATCH_SIZE"):
            settings.DJ_CKE_BULK_CREATE_BATCH_SIZE: int = 50  # type: ignore[attr-defined]

        if not hasattr(settings, "DJ_CKE_CSRF_COOKIE_NAME"):
            settings.DJ_CKE_CSRF_COOKIE_NAME: str = settings.CSRF_COOKIE_NAME  # type: ignore[attr-defined]

        if not hasattr(settings, "DJ_CKE_CUSTOM_COLOUR_PALETTE"):
            settings.DJ_CKE_CUSTOM_COLOUR_PALETTE: list = [  # type: ignore[attr-defined]
                {"color": "hsl(4, 90%, 58%)", "label": "Red"},
                {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
                {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
                {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
                {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
                {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
            ]

        if not hasattr(settings, "DJ_CKE_CUSTOM_CSS"):
            settings.DJ_CKE_CUSTOM_CSS: str = ""  # type: ignore[attr-defined]

        if not hasattr(settings, "DJ_CKE_IMAGE_FORMATTER"):
            settings.DJ_CKE_IMAGE_FORMATTER = (
                "django_ckeditors.image.convert_image_to_webp"
            )
        if not hasattr(settings, "DJ_CKE_FORMAT_IMAGE"):
            settings.DJ_CKE_FORMAT_IMAGE = True  # False: keep original formt and name.

        # Either delete or store Images not in the editor.  These are
        # images added and then removed from the editor. The image will
        # persist in storage unless handled outside the editor.
        if not hasattr(settings, "DJ_CKE_IMAGE_DELETION"):
            settings.DJ_CKE_IMAGE_DELETION: bool = True  # type: ignore[attr-defined]

        if not hasattr(settings, "DJ_CKE_IMAGE_URL_HANDLER"):
            settings.DJ_CKE_IMAGE_URL_HANDLER: str = ""  # type: ignore[attr-defined]

        if not hasattr(settings, "DJ_CKE_IMAGE_STORAGE"):
            settings.DJ_CKE_IMAGE_STORAGE: str = ""  # type: ignore[attr-defined]

        if not hasattr(settings, "DJ_CKE_PERMITTED_IMAGE_TYPES"):
            settings.DJ_CKE_PERMITTED_IMAGE_TYPES: list[str] = [  # type: ignore[attr-defined]
                "jpg",
                "jpeg",
                "png",
                "gif",
                "bmp",
                "webp",
                "tiff",
            ]

        if not hasattr(settings, "DJ_CKE_STAFF_ONLY_IMAGE_UPLOADS"):
            settings.DJ_CKE_STAFF_ONLY_IMAGE_UPLOADS: bool = False  # type: ignore[attr-defined]

        if not hasattr(settings, "DJ_CKE_EDITORS_CONFIGS"):
            settings.DJ_CKE_EDITORS_CONFIGS: dict = {  # type: ignore[attr-defined]
                "default": {
                    "toolbar": [
                        "heading",
                        "|",
                        "bold",
                        "italic",
                        "link",
                        "bulletedList",
                        "numberedList",
                        "blockQuote",
                        "imageUpload",
                    ],
                },
                "extends": {
                    "blockToolbar": [
                        "paragraph",
                        "heading1",
                        "heading2",
                        "heading3",
                        "|",
                        "bulletedList",
                        "numberedList",
                        "|",
                        "blockQuote",
                    ],
                    "toolbar": [
                        "heading",
                        "|",
                        "outdent",
                        "indent",
                        "|",
                        "bold",
                        "italic",
                        "link",
                        "underline",
                        "strikethrough",
                        "code",
                        "subscript",
                        "superscript",
                        "highlight",
                        "|",
                        "codeBlock",
                        "sourceEditing",
                        "insertImage",
                        "bulletedList",
                        "numberedList",
                        "todoList",
                        "|",
                        "blockQuote",
                        "imageUpload",
                        "|",
                        "fontSize",
                        "fontFamily",
                        "fontColor",
                        "fontBackgroundColor",
                        "mediaEmbed",
                        "removeFormat",
                        "insertTable",
                    ],
                    "image": {
                        "toolbar": [
                            "imageTextAlternative",
                            "|",
                            "imageStyle:alignLeft",
                            "imageStyle:alignRight",
                            "imageStyle:alignCenter",
                            "imageStyle:side",
                            "|",
                        ],
                        "styles": [
                            "full",
                            "side",
                            "alignLeft",
                            "alignRight",
                            "alignCenter",
                        ],
                    },
                    "table": {
                        "contentToolbar": [
                            "tableColumn",
                            "tableRow",
                            "mergeTableCells",
                            "tableProperties",
                            "tableCellProperties",
                        ],
                        "tableProperties": {
                            "borderColors": settings.DJ_CKE_CUSTOM_COLOUR_PALETTE,
                            "backgroundColors": settings.DJ_CKE_CUSTOM_COLOUR_PALETTE,
                        },
                        "tableCellProperties": {
                            "borderColors": settings.DJ_CKE_CUSTOM_COLOUR_PALETTE,
                            "backgroundColors": settings.DJ_CKE_CUSTOM_COLOUR_PALETTE,
                        },
                    },
                    "heading": {
                        "options": [
                            {
                                "model": "paragraph",
                                "title": "Paragraph",
                                "class": "ck-heading_paragraph",
                            },
                            {
                                "model": "heading1",
                                "view": "h1",
                                "title": "Heading 1",
                                "class": "ck-heading_heading1",
                            },
                            {
                                "model": "heading2",
                                "view": "h2",
                                "title": "Heading 2",
                                "class": "ck-heading_heading2",
                            },
                            {
                                "model": "heading3",
                                "view": "h3",
                                "title": "Heading 3",
                                "class": "ck-heading_heading3",
                            },
                        ],
                    },
                },
                "list": {
                    "properties": {
                        "styles": "true",
                        "startIndex": "true",
                        "reversed": "true",
                    },
                },
            }
