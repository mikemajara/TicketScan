#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from ticket_scan.skeleton import fib

__author__ = "Miguel López-N. Alcalde"
__copyright__ = "Miguel López-N. Alcalde"
__license__ = "proprietary"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
