"""All the errors envparse needs."""


class BaseError(Exception):
    """Base Error for when envparse fails."""

    def __init__(self, message, **extra):
        """Make a new error."""
        self.message = message
        self.extra = extra


class ParseError(BaseError):
    """Specific Error for when a raw value cannot be parsed."""


class ValidationError(BaseError):
    """Specific Error for when a parsed value in not valid."""
