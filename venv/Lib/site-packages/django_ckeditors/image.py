"""Image tools."""

from __future__ import annotations

import logging
from bisect import bisect
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageSequence


from django.core.files.uploadedfile import UploadedFile

logger = logging.getLogger(__name__)


def convert_image_to_webp(uploaded_file: UploadedFile) -> tuple[str, BytesIO]:
    """
    Converts an uploaded  validated image to WEBP format.

    Returns:
        A tuple containing the original filename with a .webp extension and
        the BytesIO stream of the converted image.
    """

    with uploaded_file.open("rb") as image_file:
        img = Image.open(image_file)

        # Handle multi-frame images (like GIFs or animated WebPs)
        if getattr(img, "is_animated", False):
            for i, frame in enumerate(ImageSequence.Iterator(img)):
                if getattr(frame, "mode", None) != "RGB":
                    img.seek(i)
                    img.paste(frame.convert("RGB"))

        # Handle single-frame images (like JPEG, PNG)
        elif getattr(img, "mode", None) != "RGB":
            img = img.convert("RGB")

        image_stream = BytesIO()
        quality = _determine_quality(uploaded_file.size)
        img.save(image_stream, format="WEBP", quality=quality, method=6)
        image_stream.seek(0)

        filename = Path(uploaded_file.name)
        webp_filename = filename.with_suffix(".webp")

        return str(webp_filename), image_stream


def _determine_quality(image_size: int) -> int:
    """Determines the optimal WebP image quality level based on file size.

    This function uses a binary search algorithm (`bisect`) to efficiently
    find the appropriate quality level based on pre-defined file size thresholds.

    Args:
        image_size: The size of the original image in bytes.

    Returns:
        The recommended quality level for WebP compression (1-100). Lower
        values mean smaller file size but potentially lower visual quality.
    """

    # File size thresholds (in bytes) and corresponding quality levels
    thresholds = [500_000, 1_000_000, 2_000_000, 10_000_000]
    qualities = [30, 20, 10, 5, 3]  # 3 is the default for sizes over 10 MB

    # Find the index where image_size would be inserted to maintain sorted order
    index = bisect(thresholds, image_size)
    # Return the corresponding quality level
    return qualities[index]
