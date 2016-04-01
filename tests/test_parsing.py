"""Test that parsing works."""
import os

from envparse import Field
from envparse import parse_dict
from envparse import parse_env


def test_simple_dict_parsing():
    """Simple test for a dict."""
    args = {
        'a_var': Field(
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
        'a_var': Field(
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
        'a_var': Field(
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
        'a_var': Field(
            use=int,
            load_from='A_VAR',
            validate=(
                bool,
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
        'a_var': Field(
            use=int,
            load_from='A_VAR',
            validate=lambda x: x == 0
        ),
        'some_string': Field(
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
        'a_var': Field(
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
        'a_var': Field(
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
        'a_bool': Field(
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
        'a_list': Field(
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