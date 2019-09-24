import copy
from typing import List

from fuzzywuzzy import fuzz

DEFAULT_SIMILARITY_TH = 70

class ResultObject:
    def __init__(self,
                 index: List[int] = [None],
                 value_search: List[str] = [],
                 value_found: List[str] = [None],
                 value_requested: any = None,
                 ratio: List[int] = [None],
                 is_found: List[bool] = [False],
                 ):
        self.index = index
        self.value_search = value_search
        self.value_found = value_found
        self.value_requested = value_requested
        self.ratio = ratio
        self.is_found = is_found

    @classmethod
    def combine_results(cls, args: List['ResultObject']):
        results = args.copy()
        first = results.pop(0)
        result_object = ResultObject(
            index=first.index,
            value_search=first.value_search,
            value_found=first.value_found,
            value_requested=first.value_requested,
            ratio=first.ratio,
            is_found=first.is_found,
        )
        for result in results:
            result_object.index = [*result_object.index, *result.index]
            result_object.value_search = [*result_object.value_search, *result.value_search]
            result_object.value_found = [*result_object.value_found, *result.value_found]
            result_object.value_requested = [*result_object.value_requested, *result.value_requested]
            result_object.ratio = [*result_object.ratio, *result.ratio]
            result_object.is_found = [*result_object.is_found, *result.is_found]
        return result_object

    def to_json(self):
        return self.__dict__

    def __eq__(self, other):
        return self.index == other.index and \
        self.value_search == other.value_search and \
        self.value_found == other.value_found and \
        self.value_requested == other.value_requested and \
        self.ratio == other.ratio and \
        self.is_found == other.is_found


def find_line_with_similarity(lines: list, string: str, similarity_th=DEFAULT_SIMILARITY_TH):
    """
    Returns the most similar line found in the ticket using Levenshtein distance.
    It is case insensitive.
    :param ticket:
    :param string:
    :param similarity_th:
    :return:
    """
    best_found_line = ResultObject(value_search=[string])
    best_ratio = 0
    for idx, line in enumerate(lines):
        ratio = fuzz.ratio(line.lower(), string.lower())
        if best_ratio < ratio > similarity_th:
            best_found_line = ResultObject(
                index=[idx],
                value_search=[string],
                value_found=[line],
                value_requested=[line],
                ratio=[ratio],
                is_found=[True],
            )
            best_ratio = ratio
    return best_found_line


def find_lines_with_limits(lines: list, upper_limit: str, lower_limit: str, similarity_th=DEFAULT_SIMILARITY_TH):
    upper_limit_line_found = find_line_with_similarity(lines, upper_limit, similarity_th)
    lower_limit_line_found = find_line_with_similarity(lines, lower_limit, similarity_th)
    result_object = ResultObject.combine_results([upper_limit_line_found, lower_limit_line_found])
    result_object.value_requested = []
    if upper_limit_line_found.is_found[0] and lower_limit_line_found.is_found[0]:
        result_object.value_requested = lines[upper_limit_line_found.index[0]+1:lower_limit_line_found.index[0]]
    return result_object


def find_lines_with_limit(lines: list,
                          limit: str,
                          amount_lines: int = 1,
                          limit_type="upper",
                          similarity_th=DEFAULT_SIMILARITY_TH):
    """
    Finds line(s) with upper/lower limit.
    :param lines:
    :param limit:
    :param amount_lines:
    :param limit_type:
    :param similarity_th:
    :return:
    """
    if amount_lines < 1:
        raise ValueError("amount lines must be greater than 1")
    limit_line_found = find_line_with_similarity(lines, limit, similarity_th)
    result_lines = copy.copy(limit_line_found)
    result_lines.value_requested = []
    if limit_line_found.is_found[0]:
        if limit_type == "upper":
            result_lines.value_requested = lines[
                limit_line_found.index[0]+1:
                limit_line_found.index[0]+1+amount_lines
            ]
        elif limit_type == "lower":
            result_lines.value_requested = lines[
                limit_line_found.index[0]-amount_lines:
                limit_line_found.index[0]
            ]
        else:
            raise ValueError("limit_type argument must be one of ['upper', 'lower']")
    return result_lines
