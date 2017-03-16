pytest-exceptional
==================


.. image:: https://img.shields.io/pypi/v/pytest-exceptional.svg
    :target: https://pypi.python.org/pypi/pytest-exceptional
.. image:: https://img.shields.io/pypi/pyversions/pytest-exceptional.svg
    :target: https://pypi.python.org/pypi/pytest-exceptional
.. image:: https://travis-ci.org/vodik/pytest-exceptional.svg?branch=master
    :target: https://travis-ci.org/vodik/pytest-exceptional
    :alt: See Build Status on Travis CI
.. image:: https://ci.appveyor.com/api/projects/status/github/vodik/pytest-exceptional?branch=master
    :target: https://ci.appveyor.com/project/vodik/pytest-exceptional/branch/master
    :alt: See Build Status on AppVeyor

Better pytest Exceptions
------------------------

This plugin attempts to make richer pytest exceptions a snap to write.
For example, consider the following exception:

.. code:: python

    class StartFire(pytest.Exception):
        __teststatus__ = 'fire', '🔥', ('FIRE', {'purple': True, 'bold': True})

        def toterminal(self, longrepr, tw):
            tw.line("FIRE! Please evacuate the building!")
            longrepr.toterminal(tw)

        def summary_header(self, header):
            return "Fire started during {}".format(header)

When this specific exception class is thrown, the pretty printing and
result categorization is now in the hands of the exception, making it
more straightforward than writing special purpose plugins.::

    ============================= test session starts ==============================
    platform linux -- Python 3.6.0, pytest-3.0.7, py-1.4.32, pluggy-0.4.0
    cachedir: .cache
    rootdir: /home/simon/src/pytest-exceptional, inifile:
    plugins: exceptional-0.1.0
    collected 1 items

    tests/test_fail_test.py::test_fire FIRE

    ________________________ Fire started during test_fire _________________________
    FIRE! Please evacuate the building!

        def test_fire():
    >       raise StartFire('There is a fire')
    E       test_fail_test.StartFire: There is a fire

    tests/test_fail_test.py:47: StartFire
    ============================ 1 fire in 0.02 seconds ============================

TODO
----

Provide more control over formatting and presentation without making
the API too cumbersome. Still very much an early prototype and
probably not close to a stable API.

Installation
------------

You can install "pytest-exceptional" via `pip`_ from `PyPI`_::

    $ pip install pytest-exceptional

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please
ensure the coverage at least stays the same before you submit a pull
request.

License
-------

Distributed under the terms of the `MIT`_ license,
"pytest-exceptional" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a
detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/vodik/pytest-exceptional/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
