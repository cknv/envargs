"""Everthing about vars."""
from . import errors
from . import helpers


class Var:
    """Representing a required var in the dictionary.

    Including the means to parse and potentially validate it.
    """

    def __init__(self, use, validate=None, load_from=None, default=None, err_msg=None):
        """Return a new instance."""
        self.use = use
        self.validate_with = helpers.callables(validate)
        self.load_from = load_from
        self.default = default
        self.err_msg = err_msg

    def __repr__(self):
        """Return the representation."""
        return '<Var use={}, validate={}, load_from={}, default={}>'.format(
            self.use,
            self.validate_with,
            self.load_from,
            self.default,
        )

    def parse(self, value, location):
        """Return the parsed value."""
        try:
            return self.use(value)
        except Exception as err:
            raise errors.ParseError(
                self.err_msg or 'Parsing failed.',
                value=value,
                location=location,
            ) from err

    def validate(self, value, location):
        """Validate the parsed value."""
        if self.validate_with is None:
            return

        for validator in self.validate_with:
            if validator(value) is False:
                raise errors.ValidationError(
                    self.err_msg or 'Validation failed.',
                    value=value,
                    location=location,
                )
