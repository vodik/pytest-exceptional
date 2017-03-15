# -*- coding: utf-8 -*-

import pytest
from _pytest._code.code import TerminalRepr


class PytestException(Exception):
    pass


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
        except:
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
    if not call.excinfo:
        return
    elif call.excinfo.errisinstance(PytestException):
        report.excinfo = call.excinfo
        report.longrepr = ExceptionRepr(report.excinfo,
                                        report.longrepr)


def pytest_report_teststatus(report):
    if hasattr(report, 'excinfo'):
        return report.excinfo.value.__teststatus__


def pytest_terminal_summary(terminalreporter):
    for cls in PytestException.__subclasses__():
        cat, _, _ = cls.__teststatus__
        for report in terminalreporter.getreports(cat):
            header = terminalreporter._getfailureheadline(report)
            report.longrepr.terminal_summary(terminalreporter, header)
