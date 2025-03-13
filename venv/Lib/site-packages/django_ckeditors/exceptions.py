class PillowImageError(Exception):
    """Catchall for when a Pillow read error is encountered."""

    def __init__(self, message, image_type=None):
        super().__init__(message)
        self.image_type = image_type


class InvalidImageTypeError(Exception):
    """Raised when an unsupported image type is encountered."""

    def __init__(self, message, image_type=None):
        super().__init__(message)
        self.image_type = image_type
