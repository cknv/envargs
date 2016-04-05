Envparse
========

Simple means of parsing and validating envvars. Heavily inspired by the earlier versions of webargs.

Installing
----------

Currently ``envparse`` is not distributed via pypi, so to get your hands on it, you will have to pip install via git.

.. code-block:: shell

    $ pip install git+git://github.com/cknv/envparse.git

Using
-----

.. code-block:: python

    from envparse import Var, parse_env

    required_vars = {
        'a_int': Var(
            use=int,
            load_from='A_VAR',
            validate=lambda x: x >= 0,
        ),
        'a_list': Var(
            use=lambda x: x.split(','),
            load_from='A_LIST',
            validate=(
                lambda x: len(x) == 2,
                lambda x: x[0] == 'first element',
            ),
        ),
    }

    parsed = parse_env(required_vars)

Why reinvent the wheel again?
-----------------------------

To be fair there are many good packages out there to parse environment variables, quite a few of them in python too. So this package can easily be seen as redundant. However, with separation of parsing and validation into two separate functions, you gain more power to control what is actually accepted, not to mention that it makes it possible to inline a few more things, as you can use simple buildins for most things and then lambdas for most validation.
