"""Smaller helper functions for taking care of repeated things."""


def callables(potential_callables):
    """Ensure that the callables are in fact a sequence."""
    if callable(potential_callables):
        return [potential_callables]

    return potential_callables
