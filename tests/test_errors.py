"""Test that parsing can fail."""
from pytest import raises

from envargs import errors
from envargs import parse_dict
from envargs import Var


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

    with raises(errors.ParseError) as err:
        parse_dict(values, args)

    assert err.value.extra == {
        'location': 'A_VAR',
        'value': 'abc',
    }


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

    with raises(errors.ValidationError) as err:
        parse_dict(values, args)

    assert err.value.extra == {
        'value': 1,
        'location': 'A_VAR',
    }


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

    with raises(errors.ParseError) as err:
        parse_dict(values, args)

    assert err.value.extra == {
        'location': 'A_VAR',
    }


def test_fancy_validation_function():
    """Test that fails to validate with a real function."""
    def validation_function(value):
        if value == 1:
            raise errors.ValidationError(
                'Value not 1',
                value=value,
            )

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

    with raises(errors.ValidationError) as err:
        parse_dict(values, args)

    assert err.value.extra == {
        'value': 1,
    }


def test_err_msg():
    """Test that error messages bubble up, when you use them."""
    args = {
        'a_var': Var(
            use=int,
            load_from='A_VAR',
            err_msg='A_VAR not valid',
        ),
    }

    values = {
        'A_VAR': 'abc',
    }

    with raises(errors.ParseError) as err:
        parse_dict(values, args)

    assert err.value.message == 'A_VAR not valid'
    assert repr(err.value) == "ParseError('A_VAR not valid',)"
