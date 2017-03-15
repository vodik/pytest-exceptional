# -*- coding: utf-8 -*-

import pytest


def test_custom_exception(testdir):
    """Make sure that pytest accepts our fixture."""

    testdir.makepyfile(u"""
        # -*- coding: utf-8 -*-

        import pytest

        class StartFire(pytest.Exception):
            __teststatus__ = 'fire', u'🔥', ('FIRE', {'purple': True, 'bold': True})

            def toterminal(self, longrepr, tw):
                tw.line("FIRE! Please evacuate the building!")
                longrepr.toterminal(tw)

            def summary_header(self, header):
                return "Fire started during {}".format(header)

        def test_start_fire():
            raise StartFire('This is a fire')
    """)

    result = testdir.runpytest('-v')

    result.stdout.fnmatch_lines([
        '*::test_start_fire FIRE',
        'FIRE! Please evacuate the building!',
    ])
    assert result.ret == 1
