"""Everthing about vars."""
from . import errors


class Var:
    """Representing a required var in the dictionary.

    Including the means to parse and potentially validate it.
    """

    def __init__(self, use, validate=None, load_from=None, default=None, err_msg=None):
        """Return a new instance."""
        self.use = use
        self.validate_with = validate
        self.load_from = load_from
        self.default = default
        self.err_msg = err_msg

    def __repr__(self):
        """Return the representation."""
        return '<Var use={}, validate={}, load_from={} default={}>'.format(
            self.use,
            self.validate_with,
            self.load_from,
            self.default,
        )

    def parse(self, value):
        """Return the parsed value."""
        try:
            return self.use(value)
        except Exception as err:
            raise errors.ParseError(
                'Could not parse value.'
            ) from err

    def validate(self, value):
        """Validate the parsed value."""
        if self.validate_with is None:
            return

        if callable(self.validate_with):
            if self.validate_with(value) is False:
                raise errors.ValidationError(
                    self.err_msg or 'Validation failed.'
                )

        elif isinstance(self.validate_with, (list, set, tuple)):
            for validator in self.validate_with:
                if validator(value) is False:
                    raise errors.ValidationError(
                        self.err_msg or 'Validation failed.'
                    )
