"""Test that parsing works."""
import os

from envargs import parse_dict
from envargs import parse_env
from envargs import Var


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
    def parse_bool(value):
        return value.lower() in {
            'true',
            'yes',
            'y',
            '1',
        }

    args = {
        'a_bool': Var(
            use=parse_bool,
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
    def parse_list(value):
        return [
            int(each)
            for each in value.split(',')
        ]

    args = {
        'a_list': Var(
            use=parse_list,
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
            use=lambda x: x.lower() in {'1', 't', 'true'},
            validate=lambda x: isinstance(x, bool),
            default=False,
        ),
    }

    values = {}

    assert parse_dict(values, args) == {
        'a_bool': False,
    }


def test_nesting():
    """Make sure we can parse nested structures."""
    args = {
        'nested': {
            'a_str': Var(use=str),
            'an_int': Var(use=int),
        },
    }

    values = {
        'a_str': 'this-is-my-string',
        'an_int': '10'
    }

    assert parse_dict(values, args) == {
        'nested': {
            'a_str': 'this-is-my-string',
            'an_int': 10,
        },
    }


def test_static_vars():
    """Test that hardcoded vars fall through parsing."""
    args = {
        'a_var': Var(
            use=int,
            load_from='A_VAR',
        ),
        'some_bytes': b'bytes!',
        'a_string': 'my string',
        'a_float': 1.5,
        'a_int': 1,
        'a_bool': True,
    }

    values = {
        'A_VAR': '0',
    }

    assert parse_dict(values, args) == {
        'a_var': 0,
        'some_bytes': b'bytes!',
        'a_string': 'my string',
        'a_float': 1.5,
        'a_int': 1,
        'a_bool': True,
    }
