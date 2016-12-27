Envargs
========

.. image:: https://travis-ci.org/cknv/envargs.svg?branch=master
    :target: https://travis-ci.org/cknv/envargs

.. image:: https://coveralls.io/repos/github/cknv/envargs/badge.svg?branch=master
    :target: https://coveralls.io/github/cknv/envargs?branch=master

Simple means of parsing and validating environment variables. Heavily inspired by the earlier versions of webargs, which also explains the name to some extend.

Installing
----------

.. code-block:: shell

    $ pip install envargs

Using
-----

.. code-block:: python

    from envargs import Var, parse_env

    required_vars = {
        'A_INT': Var(
            use=int,
            validate=lambda x: x >= 0,
        ),
        'A_LIST': Var(
            use=lambda x: x.split(','),
            validate=(
                lambda x: len(x) == 2,
                lambda x: x[0] == 'first element',
            ),
        ),
        'A_STR': Var(
            use=str,
            load_from='SOME_OTHER_NAME',
            validate=bool,
        ),
    }

    parsed = parse_env(required_vars)

Say you want to configure your Flask app using this:

.. code-block:: python

    app.config.from_mapping(parsed)

Why reinvent the wheel again?
-----------------------------

To be fair there are many good packages out there to parse environment variables, quite a few of them in python too. So this package can easily be seen as redundant. However, with separation of parsing and validation into two separate functions, you gain more power to control what is actually accepted, not to mention that it makes it possible to inline a few more things, as you can most often get away with using builtin functions for most parsing and validation, and when that is not enough, lambdas or partials can do the rest.
