# -*- coding: utf-8 -*-

import pytest


def test_custom_exception(testdir):
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


def test_makereport(testdir):
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

        def test_start_fire(request):
            StartFire.makereport(request.node, 'This is a fire', when='mid-test')
    """)

    result = testdir.runpytest('-v')

    result.stdout.fnmatch_lines([
        '*::test_start_fire FIRE',
        '*::test_start_fire PASSED',
    ])
    assert result.ret == 1
