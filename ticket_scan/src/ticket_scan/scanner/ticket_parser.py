import os
import json
import copy
from typing import List, Type
import numpy as np
import logging
import requests
from fuzzywuzzy import fuzz
from ticket_scan.scanner.helpers import setup_logging

DEFAULT_SIMILARITY_TH = 70
URL_TICKET_STORE = "http://localhost:5001"
END_POINT_COMPANIES = "get_companies"
END_POINT_STORES = "get_stores"

METHOD_CARD_STRING = "CARD"
METHOD_CASH_STRING = "CASH"

logger = logging.getLogger(__name__)
setup_logging(logging.DEBUG)

# Dummy variables
example_ticket = {
    "0": "MERCADONA S.A.",
    "1": "C/ MAYOR, 7 - ESPINARLO",
    "2": ". MURCIA",
    "3": "TELEFONO: 968307114",
    "4": "NIF. A-46103834",
    "5": "7/03/2019 19:51 OP: 1059346",
    "6": "FACTURA SIMPLIFICADA: 2308-011-v43UTO",
    "7": "Preciu Importe",
    "8": "Vescr ipción unidad (€)",
    "9": "1 B,ALMENDRA S/A 8,40",
    "10": "4 L SEMI S/LACTO 4,50 16,00",
    "11": "3 GALLETA RELTEV 1,22 3,06",
    "12": "1 COPOS AVENA 0,81",
    "13": "1 COSTILLA BARB 3,99",
    "14": "1 ZANAHORIA BOLS 0,69",
    "15": "2 VENTRESCA ATUN 2,15 4,30",
    "16": "1 PAPEL HIGIENIC 2,70",
    "17": "1 HIGIENICO DOBL 2,01",
    "18": "1 PEPINO o",
    "19": "U,478 ky 1,89 €/kg u,9uU",
    "20": "1 PLATANO",
    "21": "0,616 kg 2,29 €e/kg 1,41",
    "22": "TOTAL 463%",
    # "222": "ENTREGA...EFECTIVO 50,00",
    # "2222": "DEVOLUCIÓN 0,05",
    "23": "TARJETA. BANCARIA 46%",
    "24": "LLTALLE (€)",
    "25": "IA BASE IMPONIBLE CUOTA",
    "26": "4% 20,19 0,81",
    "27": "10% 19,24 1,92",
    "28": "2 3,94 0,83",
    "29": "HITAL 43,9 3,56",
    "30": "LARJ: 9016",
    "31": "AUT: 307029",
    "32": "“ul: 44101236",
    "33": "+ PALO TARJETA BANCARIA +",
    "34": "- 4490000031010",
    "35": "«IVA CLÁSICA",
    "36": "30",
    "37": "SE ADMIIEN DEVOLUCIONES CON TICKEf"
}
available_stores = [
    {
        "_id": "5d7683401855750cd80a8057",
        "address": "AVDA. CICLISTA MARIANO ROJAS-AV",
        "city": "Murcia",
        "company_id": "5d76824c1855750cd80a8037",
        "country": "Spain",
        "phone": "968392509"
    },
    {
        "_id": "5d8742d3dcad30c5cc30624d",
        "address": "C/ MAYOR, 7 - ESPINARDO",
        "city": "Murcia",
        "company_id": "5d76824c1855750cd80a8037",
        "country": "Spain",
        "phone": "968392509"
    },
    {
        "_id": "5d87822cdcad30c5cc30740a",
        "address": "Paseo Floridablanca, 4",
        "city": "Murcia",
        "company_id": "5d76824c1855750cd80a8037",
        "country": "Spain",
        "phone": "968392509"
    }
]
available_companies = [
    {
        "_id": "5d76824c1855750cd80a8037",
        "name": "MERCADONA S.A.",
        "taxId": "A-46103834",
        "web": None
    },
    {
        "_id": "5d7682a11855750cd80a8040",
        "name": "LIDL",
        "taxId": "A60195278",
        "web": "www.lidl.es"
    }
]

store_name = "MERCADONA S.A."
list_upper_limit = "Descripción unidad (€)"
list_lower_limit = "TOTAL "


# TODO set searches or defaults for specific ticket.
line_street = "C/ MAYOR, 7 - ESPINARLO"
line_city = "o MURCIA"
line_telephone = "TELEFONO; 9568307114"
line_store_id = "NIF: A-46103834"
line_fra = "HACTURA SIMPLIFICADA: 2308-011-643UT6"
line_cash = "ENTREGA...EFECTIVO "
line_returned = "DEVOLUCIÓN "
line_card = "TARJETA..BANCARIA "
# ...

date_upper_limit = "" # In this case nif string...


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


def find_company(lines: list, available_companies: list, similarity_th=DEFAULT_SIMILARITY_TH):
    result_object = ResultObject()
    values_searched = []
    best_ratio = 0
    for company in available_companies:
        found_company = find_line_with_similarity(lines, company["name"], similarity_th)
        values_searched.append(found_company.value_search[0])
        if found_company.is_found[0] and best_ratio < found_company.ratio[0] > similarity_th:
            result_found = copy.copy(found_company)
            result_object = result_found
            result_object.value_search = values_searched
            result_object.value_requested = company
            best_ratio = result_found.ratio[0]
    return result_object


def find_store(lines: list, available_stores: list, similarity_th=DEFAULT_SIMILARITY_TH):
    result_object = ResultObject()
    values_searched = []
    best_ratio_address = 0
    best_ratio_city = 0

    for store in available_stores:
        found_address = find_line_with_similarity(lines, store["address"])
        found_city = find_line_with_similarity(lines, store["city"])

        values_searched.append(found_address.value_search[0])
        values_searched.append(found_city.value_search[0])

        if found_address.is_found[0] and found_city.is_found[0] and \
                best_ratio_address < found_address.ratio[0] > similarity_th and \
                best_ratio_city < found_city.ratio[0] > similarity_th:
            result_found = copy.copy(ResultObject.combine_results([found_address, found_city]))

            result_object = result_found
            result_object.value_search = values_searched
            result_object.value_requested = store

            best_ratio_address = found_address.ratio[0]
            best_ratio_city = found_city.ratio[0]
    return result_object


def find_payment_method(lines: list):
    found_method = find_lines_with_limit(lines, limit=list_lower_limit, amount_lines=1, limit_type="upper")
    if found_method.is_found[0]:
        found_card = find_line_with_similarity(lines, line_card)
        found_cash = find_line_with_similarity(lines, line_cash)
        if found_card.is_found[0]:
            found_method.value_requested = [METHOD_CARD_STRING]
            return ResultObject.combine_results([found_method, found_card])
        elif found_cash.is_found[0]:
            found_method.value_requested = [METHOD_CASH_STRING]
            found_returned = find_lines_with_limit(
                lines,
                limit=found_cash.value_found[0],
                amount_lines=1,
                limit_type="upper"
            )
            return ResultObject.combine_results([found_method, found_cash, found_returned])
        else:
            return ResultObject(value_search=[list_lower_limit])
    else:
        return ResultObject(value_search=[list_lower_limit])


def find_lines_address(lines: list, company: dict):
    # Mercadona proprietary
    return find_lines_with_limit(lines, company["name"], amount_lines=2, limit_type="upper")


# TODO refactor
def parse(ticket: dict):
    ticket_response = {}
    company = None
    store = None
    lines = list(ticket.values())

    # 1.- Find company
    r = requests.get(os.path.join(URL_TICKET_STORE, END_POINT_COMPANIES))
    available_companies = r.json()
    found_company = find_company(
        lines,
        available_companies
    )
    # company = next(filter(lambda x: found_company.value_requested[0] == x["name"], available_companies), None)
    company = found_company.value_requested if found_company.is_found[0] else None

    if company is None:
        raise Exception("Company not found")

    # 2.- Find store
    r = requests.get(os.path.join(URL_TICKET_STORE,END_POINT_STORES, company["_id"]))
    available_stores = r.json()
    found_address_lines = find_lines_address(lines, company)
    found_store = find_store(found_address_lines.value_requested, available_stores)
    # store = available_stores[found_store["index"]] if found_store else None
    store = found_store.value_requested if found_store.is_found[0] else None

    if store is None:
        raise Exception("Store not found")

    # 3.- Fecha
    found_date = find_lines_with_limit(lines, limit=company["taxId"], amount_lines=1, limit_type="upper")

    # 4.- Lineas de compra
    found_product_lines = find_lines_with_limits(lines, list_upper_limit, list_lower_limit)

    # 5.- Total y método de pago
    found_total_line = find_line_with_similarity(lines, list_lower_limit)
    found_payment_method = find_payment_method(lines)
    payment = {
        "total": found_total_line.value_requested[0],
        "method": found_payment_method.value_requested[0],
        # TODO add return
    }

    # 6.- Build ticket
    ticket_response["company"] = company
    ticket_response["store"] = store
    ticket_response["date"] = found_date.value_requested[0]
    ticket_response["lines"] = found_product_lines.value_requested
    ticket_response["payment"] = payment
    print(json.dumps(ticket_response, indent=2, default=str, ensure_ascii=False))
    return ticket_response

def print_json(string):
    print(json.dumps(string, indent=2, ensure_ascii=False))

# parse(example_ticket)
# lines = list(example_ticket.values())
# print_json(find_lines_with_limits(lines, "list_upper_limit", list_lower_limit).to_json())
# print_json(find_lines_with_limit(lines, line_store_id, amount_lines=1, limit_type="upper").to_json())
# print_json(find_lines_with_limit(lines, line_fra, amount_lines=1, limit_type="lower").to_json())
# print_json(find_company(lines, available_companies=available_companies).to_json())
# print_json(find_store(lines, available_stores).to_json())
# print_json(find_payment_method(lines).to_json())
# print_json(find_lines_address(lines, company=available_companies[0]).to_json())