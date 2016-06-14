"""Test that parsing can fail."""
from envargs import Var


def test_var_repr():
    """Test repr of the Var class."""
    var = Var(
        use=str,
        validate=bool,
        load_from='some_var',
    )

    expected = (
        '<Var use=<class \'str\'>, '
        'validate=[<class \'bool\'>], '
        'load_from=some_var, '
        'default=None>'
    )

    assert repr(var) == expected
