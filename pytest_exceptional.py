# -*- coding: utf-8 -*-

import time
import pytest
from _pytest._code.code import TerminalRepr, ExceptionInfo


class RecordFailure:
    """Mock pytest internal reporter to emulate CallInfo.

    Creates a class that can be safely passed into
    pytest_runtest_makereport to add failure report based on an
    arbitrary exception.
    """
    def __init__(self, exception, when="setup"):
        self.when = when
        self.start = time.time()
        self.stop = time.time()

        # We need to generate a traceback to continue. ExceptionInfo
        # calls sys.exc_info() internally
        try:
            raise exception
        except Exception:
            self.excinfo = ExceptionInfo()


class PytestException(Exception):
    @classmethod
    def makereport(cls, item, *args, **kwargs):
        when = kwargs.pop('when', 'setup')
        call = RecordFailure(cls(*args, **kwargs), when=when)
        hook = item.ihook
        report = hook.pytest_runtest_makereport(item=item, call=call)
        hook.pytest_runtest_logreport(report=report)


class ExceptionRepr(TerminalRepr):
    def __init__(self, excinfo, longrepr):
        self.excinfo = excinfo
        self.longrepr = longrepr

    def toterminal(self, tw):
        try:
            self.excinfo.value.toterminal(self.longrepr, tw)
        except AttributeError:
            self.longrepr.toterminal(tw)

    def terminal_summary(self, terminalreporter, header):
        try:
            header = self.excinfo.value.summary_header(header)
        except AttributeError:
            pass

        _, _, word = self.excinfo.value.__teststatus__
        terminalreporter.write_sep('_', header, **word[1])
        self.toterminal(terminalreporter._tw)


def pytest_namespace():
    return {'Exception': PytestException}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if call.excinfo and call.excinfo.errisinstance(PytestException):
        report.excinfo = call.excinfo
        report.longrepr = ExceptionRepr(report.excinfo,
                                        report.longrepr)


def pytest_report_teststatus(report):
    if hasattr(report, 'excinfo'):
        return getattr(report.excinfo.value, '__teststatus__', None)


def pytest_terminal_summary(terminalreporter):
    categories = set()
    for cls in PytestException.__subclasses__():
        teststatus = getattr(cls, '__teststatus__', None)
        if teststatus:
            categories.add(teststatus[0])

    for cat in categories:
        for report in terminalreporter.getreports(cat):
            header = terminalreporter._getfailureheadline(report)
            report.longrepr.terminal_summary(terminalreporter, header)
