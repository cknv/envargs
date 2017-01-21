"""Default value parsers. Does common things simply."""


def boolean(value):
    """Return true if the value indicates a truthiness."""
    options = {
        'true',
        't',
        '1',
        'yes',
    }

    return value.lower() in options
