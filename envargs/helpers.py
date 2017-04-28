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


def split_by(separator, converter=None):
    """Return the value split by commas."""
    def splitter(value):
        return [
            converter(each) if converter else each
            for each in value.split(',')
        ]

    return splitter
