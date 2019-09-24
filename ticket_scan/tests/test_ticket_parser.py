#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from ticket_scan.scanner import ticket_parser
from ticket_parser import ResultObject
from tests import ticket_provider

__author__ = "Miguel López-N. Alcalde"
__copyright__ = "Miguel López-N. Alcalde"
__license__ = "proprietary"



def test_find_line_with_similarity_identical_strings_should_return_100():
    lines = ticket_provider.get_dummy_ticket_lines()
    line_to_search = "MERCADONA S.A."
    expected_result = ResultObject(
        index=[0],
        value_search=[line_to_search],
        value_found=["MERCADONA S.A."],
        value_requested=["MERCADONA S.A."],
        ratio=[100],
        is_found=[True]
    )
    obtained_result = ticket_parser.find_line_with_similarity(lines, line_to_search)
    assert expected_result == obtained_result


def test_find_line_with_similarity_identical_different_case_strings_should_return_100():
    lines = ticket_provider.get_dummy_ticket_lines()
    line_to_search = "mercadona S.A."
    expected_result = ResultObject(
        index=[0],
        value_search=[line_to_search],
        value_found=["MERCADONA S.A."],
        value_requested=["MERCADONA S.A."],
        ratio=[100],
        is_found=[True]
    )
    obtained_result = ticket_parser.find_line_with_similarity(lines, line_to_search)
    assert expected_result == obtained_result


def test_find_line_with_similarity_identical_special_chars_strings_should_return_100():
    lines = ticket_provider.get_dummy_ticket_lines()
    line_to_search = "0,616 kg 2,29 €e/kg 1,41"
    expected_result = ResultObject(
        index=[21],
        value_search=[line_to_search],
        value_found=["0,616 kg 2,29 €e/kg 1,41"],
        value_requested=["0,616 kg 2,29 €e/kg 1,41"],
        ratio=[100],
        is_found=[True]
    )
    obtained_result = ticket_parser.find_line_with_similarity(lines, line_to_search)
    assert expected_result == obtained_result
