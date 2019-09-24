import copy
import json
from ticket_scan.scanner import line_finder as lf
from line_finder import ResultObject
from base_ticket_parser import BaseTicketParser

DEFAULT_SIMILARITY_TH = 70

# TICKET LINE REFERENCES
STR_COMPANY_NAME = "MERCADONA S.A."
STR_COMPANY_TAX_ID = "NIF: A-46103834"
STR_PRODUCT_LIST_UPPER_LIMIT = "Descripción unidad (€)"
STR_PRODUCT_LIST_LOWER_LIMIT = "TOTAL "
STR_TOTAL = "TOTAL "
STR_CARD = "TARJETA..BANCARIA "
STR_CASH = "ENTREGA...EFECTIVO "
STR_RETURNED = "DEVOLUCIÓN "

METHOD_CARD_STRING = "CARD"
METHOD_CASH_STRING = "CASH"


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


class MercadonaTicketParser(BaseTicketParser):
    @property
    def company_name(self):
        return STR_COMPANY_NAME

    @property
    def company_tax_id(self):
        return STR_COMPANY_TAX_ID

    def find_company(self, lines: list, available_companies: list, similarity_th=DEFAULT_SIMILARITY_TH):
        result_object = ResultObject()
        values_searched = []
        best_ratio = 0
        for company in available_companies:
            found_company = lf.find_line_with_similarity(lines, company["name"], similarity_th)
            values_searched.append(found_company.value_search[0])
            if found_company.is_found[0] and best_ratio < found_company.ratio[0] > similarity_th:
                result_found = copy.copy(found_company)
                result_object = result_found
                result_object.value_search = values_searched
                result_object.value_requested = company
                best_ratio = result_found.ratio[0]
        return result_object

    def find_store(self, lines: list, available_stores: list, similarity_th=DEFAULT_SIMILARITY_TH):
        result_object = ResultObject()
        values_searched = []
        best_ratio_address = 0
        best_ratio_city = 0

        for store in available_stores:
            found_address = lf.find_line_with_similarity(lines, store["address"])
            found_city = lf.find_line_with_similarity(lines, store["city"])

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

    def find_payment_method(self, lines: list):
        found_method = lf.find_lines_with_limit(
            lines,
            limit=STR_PRODUCT_LIST_LOWER_LIMIT,
            amount_lines=1,
            limit_type="upper"
        )
        if found_method.is_found[0]:
            found_card = lf.find_line_with_similarity(lines, STR_CARD)
            found_cash = lf.find_line_with_similarity(lines, STR_CASH)
            if found_card.is_found[0]:
                found_method.value_requested = [METHOD_CARD_STRING]
                return ResultObject.combine_results([found_method, found_card])
            elif found_cash.is_found[0]:
                found_method.value_requested = [METHOD_CASH_STRING]
                found_returned = lf.find_lines_with_limit(
                    lines,
                    limit=found_cash.value_found[0],
                    amount_lines=1,
                    limit_type="upper"
                )
                return ResultObject.combine_results([found_method, found_cash, found_returned])
            else:
                return ResultObject(value_search=[STR_PRODUCT_LIST_LOWER_LIMIT])
        else:
            return ResultObject(value_search=[STR_PRODUCT_LIST_LOWER_LIMIT])

    def find_lines_address(self, lines: list, company: dict):
        # Mercadona proprietary
        return lf.find_lines_with_limit(lines, company["name"], amount_lines=2, limit_type="upper")

    def parse(self, ticket: dict):
        ticket_response = {}
        company = None
        store = None
        lines = list(ticket.values())

        # 1.- Find company
        found_company = self.find_company(
            lines,
            self.get_available_companies()
        )
        # company = next(filter(lambda x: found_company.value_requested[0] == x["name"], available_companies), None)
        company = found_company.value_requested if found_company.is_found[0] else None

        if company is None:
            raise Exception("Company not found")

        # 2.- Find store
        available_stores = self.get_available_stores(company["_id"])
        found_address_lines = self.find_lines_address(lines, company)
        found_store = self.find_store(found_address_lines.value_requested, available_stores)
        # store = available_stores[found_store["index"]] if found_store else None
        store = found_store.value_requested if found_store.is_found[0] else None

        if store is None:
            raise Exception("Store not found")

        # 3.- Fecha
        found_date = lf.find_lines_with_limit(lines, limit=company["taxId"], amount_lines=1, limit_type="upper")

        # 4.- Lineas de compra
        found_product_lines = lf.find_lines_with_limits(
            lines,
            STR_PRODUCT_LIST_UPPER_LIMIT,
            STR_PRODUCT_LIST_LOWER_LIMIT
        )

        # 5.- Total y método de pago
        found_total_line = lf.find_line_with_similarity(lines, STR_PRODUCT_LIST_LOWER_LIMIT)
        found_payment_method = self.find_payment_method(lines)
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

mercadona_ticket_parser = MercadonaTicketParser()
mercadona_ticket_parser.parse(example_ticket)