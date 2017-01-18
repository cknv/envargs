"""Everything about parsing."""
import os

from . import errors


def _load_values(values, fields):
    """Load values according to the fields."""
    for dest, field in fields.items():
        location = field.load_from or dest
        value = values.get(location)

        if value is None:
            if field.default is None:
                raise errors.ParseError(
                    'Required field "{}" missing.'.format(location),
                    location=location,
                )

            yield dest, field.default

        else:
            value = field.parse(value, location)
            field.validate(value, location)
            yield dest, value


def parse_dict(values, fields):
    """Return the parsed and validated dict."""
    return {
        key: value
        for key, value in _load_values(values, fields)
    }


def parse_env(fields):
    """Return the parsed and validated environment."""
    return parse_dict(os.environ, fields)
