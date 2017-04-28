"""Test that parsing works."""
import os

from envargs import parse_dict
from envargs import parse_env
from envargs import Var
from envargs import helpers


def test_simple_dict_parsing():
    """Simple test for a dict."""
    args = {
        'a_var': Var(
            use=int,
            load_from='A_VAR',
        ),
    }

    values = {
        'A_VAR': '0',
    }

    assert parse_dict(values, args) == {
        'a_var': 0,
    }


def test_simple_envvar_parsing():
    """Simple test for preset envvars."""
    args = {
        'a_var': Var(
            use=int,
            load_from='A_VAR',
        ),
    }

    os.environ['A_VAR'] = '0'

    assert parse_env(args) == {
        'a_var': 0,
    }


def test_validation_with_lambda():
    """Test validation with a lambda."""
    args = {
        'a_var': Var(
            use=int,
            load_from='A_VAR',
            validate=lambda x: x == 0
        ),
    }

    values = {
        'A_VAR': '0',
    }

    assert parse_dict(values, args) == {
        'a_var': 0,
    }


def test_multi_validation():
    """Test multiple validation functions."""
    args = {
        'a_var': Var(
            use=int,
            load_from='A_VAR',
            validate=(
                bool,
                lambda x: x > 9,
                lambda x: x < 11,
                lambda x: x == 10,
            ),
        ),
    }

    values = {
        'A_VAR': '10',
    }

    assert parse_dict(values, args) == {
        'a_var': 10,
    }


def test_many_values():
    """Test parsing of several values work."""
    args = {
        'a_var': Var(
            use=int,
            load_from='A_VAR',
            validate=lambda x: x == 0
        ),
        'some_string': Var(
            use=lambda x: x.lower(),
            load_from='SOME_STRING',
        ),
    }

    values = {
        'A_VAR': '0',
        'SOME_STRING': 'SOME VALUE!',
    }

    assert parse_dict(values, args) == {
        'a_var': 0,
        'some_string': 'some value!',
    }


def test_default():
    """Test that setting a default works."""
    args = {
        'a_var': Var(
            use=int,
            load_from='A_VAR',
            default=5,
        ),
    }

    values = {}

    assert parse_dict(values, args) == {
        'a_var': 5,
    }


def test_default_name():
    """Test that using the default name works too."""
    args = {
        'a_var': Var(
            use=int,
        ),
    }

    values = {
        'a_var': '5',
    }

    assert parse_dict(values, args) == {
        'a_var': 5,
    }


def test_custom_function_boolean():
    """Test that we can use a custom function to parse with."""
    args = {
        'a_bool': Var(
            use=helpers.boolean,
            validate=lambda parsed: isinstance(parsed, bool)
        ),
    }

    values = {
        'a_bool': 'true',
    }

    assert parse_dict(values, args) == {
        'a_bool': True,
    }


def test_custom_function_int_list():
    """Test that we can have more complex parsing functions."""
    args = {
        'a_list': Var(
            use=helpers.split_by(',', converter=int),
            validate=(
                lambda parsed: isinstance(parsed, list),
                lambda parsed: all(isinstance(each, int) for each in parsed),
            ),
        ),
    }

    values = {
        'a_list': '1,2,3,4',
    }

    assert parse_dict(values, args) == {
        'a_list': [1, 2, 3, 4],
    }


def test_complex_defaulting():
    """Test that when defaulting, the functions are not used."""
    args = {
        'a_bool': Var(
            use=helpers.boolean,
            validate=lambda x: isinstance(x, bool),
            default=False,
        ),
    }

    values = {}

    assert parse_dict(values, args) == {
        'a_bool': False,
    }


def test_setting_value():
    """Test parsing with a lambda."""
    args = {
        'a_set': Var(
            use=lambda x: set(x.split(',')),
            validate=lambda x: isinstance(x, set),
        ),
    }

    values = {
        'a_set': 'one,two',
    }

    assert parse_dict(values, args) == {
        'a_set': {'one', 'two'},
    }
