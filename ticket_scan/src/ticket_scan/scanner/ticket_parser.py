import os
import numpy as np
import logging
import requests
from fuzzywuzzy import fuzz
from helpers import setup_logging

DEFAULT_SIMILARITY_TH = 75
URL_TICKET_STORE = "http://localhost:5001"
END_POINT_COMPANIES = "get_companies"
END_POINT_STORES = "get_stores"

logger = logging.getLogger(__name__)
setup_logging(logging.DEBUG)

# Dummy variables
example_ticket = {
    '0': 'MERCADONA S.A.',
    '1': 'C/ MAYOR, 7 - ESPINARLO',
    '2': 'o MURCIA',
    '3': 'TELEFONO; 9568307114',
    '4': 'NIF: A-46103834',
    '5': '17/63/2019 19:51 OP: 1059346',
    '6': 'HACTURA SIMPLIFICADA: 2308-011-643UT6',
    '7': 'Preciu Importe',
    '8': 'Vescripción unidad (€)',
    '9': '1 B,ALMENDRA S/A 8,40',
    '10': '4 L SEMI S/LACTO 4,50 16,00',
    '11': '3 GALLETA RELTEV 1,22 3,66',
    '12': '1 COPOS AVENA 0,81',
    '13': '1 COSTILLA BARB 3,99',
    '14': '1 ZANAHORIA BOLS 0,69',
    '15': '2 VENTRESCA ATUN 2,15 4,30',
    '16': '1 PAPEL HIGIENIC 2,70',
    '17': '1 HIGIÉNICO DOBL 2,07',
    '18': '1 PEPINO y o',
    '19': '0,418 kg 1,89 €/kg ug',
    '20': '1 PLATANO o',
    '21': '0,616 kg 2,29 e/ky 1,41',
    '22': 'TOTAL 49',
    '23': 'LILTALLE (€)',
    '24': '1YA BASE IMPONIBLE CUOTA',
    '25': '4% 20,19 0,81',
    '26': '10% 19,24 1,92',
    '27': '2% 3,94 0,83',
    '28': 'DUTAL 43,97 3,56',
    '29': 'A',
    '30': 'AUT: 307029',
    '31': 'uz 44101236',
    '32': '+ PAGO TARJETA BANCARIA +',
    '33': '- YUYODO3 101',
    '34': '«13A CLASICA',
    '35': 'SE ADMLIEN DEVOLUCIONES CON TiCkEf'
}
available_stores = ["Mercadona", "Lidl"]

store_name = "MERCADONA S.A."
list_upper_limit = "Descripción unidad (€)"
list_lower_limit = "TOTAL "


# TODO set searches or defaults for specific ticket.
line_street = "C/ MAYOR, 7 - ESPINARLO"
line_city = "o MURCIA"
line_telephone = "TELEFONO; 9568307114"
line_store_id = "NIF: A-46103834"
line_fra = "HACTURA SIMPLIFICADA: 2308-011-643UT6"
# ...

date_upper_limit = "" # In this case nif string...


def find_line_with_similarity(lines: list, string: str, similarity_th=DEFAULT_SIMILARITY_TH):
    """
    Returns the most similar line found in the ticket using Levenshtein distance.
    It is case insensitive.
    :param ticket:
    :param string:
    :param similarity_th:
    :return:
    """
    found_lines = []
    for idx, line in enumerate(lines):
        ratio = fuzz.ratio(line.lower(), string.lower())
        if ratio > similarity_th:
            found_lines.append(
                {
                    "index": idx,
                    "value_search": string,
                    "value_found": line,
                    "ratio": ratio
                }
            )
    if len(found_lines) <= 0:
        return {}
    return max(found_lines, key=lambda x: x["ratio"])


def find_lines_with_limits(lines: list, upper_limit: str, lower_limit: str, similarity_th=DEFAULT_SIMILARITY_TH):
    upper_limit_line_found = find_line_with_similarity(lines, upper_limit, similarity_th)
    lower_limit_line_found = find_line_with_similarity(lines, lower_limit, similarity_th)
    if upper_limit_line_found and lower_limit_line_found:
        upper_idx = int(upper_limit_line_found["index"])
        lower_idx = int(lower_limit_line_found["index"])
        return lines[upper_idx+1:lower_idx]
    else:
        if len(upper_limit_line_found) <= 0:
            logger.debug("upper limit line not found")
        if len(lower_limit_line_found) <= 0:
            logger.debug("lower limit line not found")
        return []


def find_lines_with_limit(lines: list,
                          limit: str,
                          amount_lines: int=1,
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
    limit_line_found = find_line_with_similarity(lines, limit, similarity_th)
    if limit_line_found:
        index_found = limit_line_found["index"]
        if limit_type == "upper":
            return lines[index_found+1:index_found+1+amount_lines]
        elif limit_type == "lower":
            return lines[index_found-amount_lines:index_found]
        else:
            raise ValueError("limit_type argument must be one of ['upper', 'lower']")


def find_company(lines: list, available_companies: list, similarity_th=DEFAULT_SIMILARITY_TH):
    found_companies = []
    for store in available_companies:
        found_line_company = find_line_with_similarity(lines, store, similarity_th)
        if found_line_company and found_line_company["ratio"] > similarity_th:
            found_companies.append(found_line_company)
    return max(found_companies, key=lambda x: x["ratio"])


def find_store(lines: list, available_stores: list, similarity_th=DEFAULT_SIMILARITY_TH):
    found_stores = []

    for idx, store in enumerate(available_stores):
        found_line_address = find_line_with_similarity(lines, store["address"])
        found_line_city = find_line_with_similarity(lines, store["city"])
        if found_line_address and found_line_city and \
            found_line_address["ratio"] > similarity_th and found_line_city["ratio"] > similarity_th:
            found_stores.append(
                {
                    "index": idx,
                    "values_search": lines,
                    "values_found": [found_line_address, found_line_city],
                    "ratio": np.average([found_line_address["ratio"], found_line_city["ratio"]])
                }
            )
    if len(found_stores) <= 0:
        return []
    return max(found_stores, key=lambda x: x["ratio"])


def find_line_address(lines: list, company: dict):
    # Mercadona proprietary
    return find_lines_with_limit(lines, company["name"], amount_lines=2, limit_type="upper")

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
        list(map(lambda x: x["name"], available_companies))
    )
    company = next(filter(lambda x: found_company["value_search"] == x["name"], available_companies), None)

    # 2.- Find store
    r = requests.get(os.path.join(URL_TICKET_STORE,END_POINT_STORES,company["_id"]))
    available_stores = r.json()
    ticket_address_lines = find_line_address(lines, company)
    found_store = find_store(ticket_address_lines, available_stores)
    store = available_stores[found_store["index"]] if found_store else None

    # 3.- Fecha
    found_date = find_lines_with_limit(lines, limit=company["taxId"], amount_lines=1, limit_type="upper")

    # 4.- Lineas de compra
    found_product_lines = find_lines_with_limits(lines, list_upper_limit, list_lower_limit)
    print(found_product_lines)

    # 5.- Build ticket
    ticket_response["company"] = company
    ticket_response["store"] = store
    ticket_response["date"] = found_date
    ticket_response["lines"] = found_product_lines
    return ticket_response


# parse_ticket(example_ticket)
# lines = list(example_ticket.values())
# print(find_lines_with_limits(lines, list_upper_limit, list_lower_limit))
# print(find_store(lines, available_stores))
# print(find_lines_with_limit(lines, line_store_id, amount_lines=1, limit_type="upper"))
# print(find_lines_with_limit(lines, line_fra, amount_lines=1, limit_type="lower"))