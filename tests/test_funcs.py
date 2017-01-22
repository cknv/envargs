"""Testing the default parser functions."""
import pytest

from envargs import inputs


@pytest.mark.parametrize('case, expected', [
    ('true', True),
    ('t', True),
    ('True', True),
    ('1', True),
    ('yes', True),
    ('0', False),
    ('false', False),
    ('no', False),
])
def test_boolean_parser(case, expected):
    """Test the default boolean parser."""
    assert inputs.boolean(case) == expected


@pytest.mark.parametrize('case, expected', [
    ('1', ['1']),
    ('1,2,3', ['1', '2', '3']),
])
def test_split_by_comma(case, expected):
    """Test the splitter."""
    assert inputs.split_by_comma(case) == expected
