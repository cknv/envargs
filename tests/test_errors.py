"""Test that parsing can fail."""
from pytest import raises

from envparse import errors
from envparse import parse_dict
from envparse import Var


def test_parse_fail():
    """Simple case that fails to parse."""
    args = {
        'a_var': Var(
            use=int,
            load_from='A_VAR',
        ),
    }

    values = {
        'A_VAR': 'abc',
    }

    with raises(errors.ParseError):
        parse_dict(values, args)


def test_validation_with_lambda_fail():
    """Simple case that fails to validate."""
    args = {
        'a_var': Var(
            use=int,
            load_from='A_VAR',
            validate=lambda x: x == 0,
        ),
    }

    values = {
        'A_VAR': '1',
    }

    with raises(errors.ValidationError):
        parse_dict(values, args)


def test_missing_value():
    """Test case that fails because of a missing value."""
    args = {
        'a_var': Var(
            use=int,
            load_from='A_VAR',
            validate=lambda x: x == 0,
        ),
    }

    values = {}

    with raises(errors.ParseError):
        parse_dict(values, args)


def test_fancy_validation_function():
    """Test that fails to validate with a real function."""
    def validation_function(value):
        if value == 1:
            raise errors.ValidationError

    args = {
        'a_var': Var(
            use=int,
            load_from='A_VAR',
            validate=validation_function,
        ),
    }

    values = {
        'A_VAR': '1',
    }

    with raises(errors.ValidationError):
        parse_dict(values, args)
