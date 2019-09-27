import copy
import json
from ticket_scan.model.company import Company, CompanySchema
from ticket_scan.model.store import StoreSchema
from ticket_scan.model.payment_information import PaymentInformation, METHOD_CARD, METHOD_CASH, PaymentInformationSchema

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

# TODO
## - [x] Move this lines to a more suitable place
##      Probably somewhere in a PaymentInformation class
# METHOD_CARD_STRING = "CARD"
# METHOD_CASH_STRING = "CASH"

# TODO
## Notes offline to pass on to trello or a notebook:
## Right now, this parser returns company and store
## as proper objects which are guaranteed to exist
## in the database.
## At some point, either this class or another
## should manage the types and checks of the other
## parts of the ticket which are currently returned
## as the strings recognized (for example, date is
## not guaranteed to be a rightful value.

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
        result = None
        best_ratio = 0
        for company in available_companies:
            found_company = lf.find_line_with_similarity(lines, company.name, similarity_th)
            if found_company.is_found[0] and best_ratio < found_company.ratio[0] > similarity_th:
                result = company
                best_ratio = found_company.ratio[0]
        return result


    # TODO refactor
    ## - [x] Only return object store
    ## - [x] Clean remaining code after returning Store Object
    ## - [ ] Make address a variable number of lines.
    def find_store(self, lines: list, available_stores: list, similarity_th=DEFAULT_SIMILARITY_TH):
        result = None
        best_ratio_address = 0
        best_ratio_city = 0

        for store in available_stores:
            found_address = lf.find_line_with_similarity(lines, store.address)
            found_city = lf.find_line_with_similarity(lines, store.city)

            if found_address.is_found[0] and found_city.is_found[0] and \
                    best_ratio_address < found_address.ratio[0] > similarity_th and \
                    best_ratio_city < found_city.ratio[0] > similarity_th:

                best_ratio_address = found_address.ratio[0]
                best_ratio_city = found_city.ratio[0]
                result = store
        return result

    def find_payment_information(self, lines: list):
        result = PaymentInformation()

        found_total = lf.find_line_with_similarity(lines, STR_TOTAL)
        if found_total.is_found[0]:
            result.total = found_total.value_requested[0]

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
                result.method = METHOD_CARD
            elif found_cash.is_found[0]:
                result.method = METHOD_CASH
                found_returned = lf.find_lines_with_limit(
                    lines,
                    limit=found_cash.value_found[0],
                    amount_lines=1,
                    limit_type="upper"
                )
                if found_returned.is_found[0]:
                    result.returned = found_returned.value_requested[0]
        return result


    def find_lines_address(self, lines: list, company: Company):
        # Mercadona proprietary
        return lf.find_lines_with_limit(lines, company.name, amount_lines=2, limit_type="upper")

    def parse(self, ticket: dict):
        ticket_response = {}
        company = None
        store = None
        lines = list(ticket.values())

        # 1.- Find company
        company = self.find_company(
            lines,
            self.get_available_companies()
        )
        # company = next(filter(lambda x: found_company.value_requested[0] == x["name"], available_companies), None)
        #company = found_company.value_requested if found_company.is_found[0] else None

        if company is None or not isinstance(company, Company):
            raise Exception("Company not found")

        # 2.- Find store
        available_stores = self.get_available_stores(company._id)
        found_address_lines = self.find_lines_address(lines, company)
        store = self.find_store(found_address_lines.value_requested, available_stores)

        if store is None:
            raise Exception("Store not found")

        # 3.- Fecha
        found_date = lf.find_lines_with_limit(lines, limit=company.taxId, amount_lines=1, limit_type="upper")

        # 4.- Lineas de compra
        found_product_lines = lf.find_lines_with_limits(
            lines,
            STR_PRODUCT_LIST_UPPER_LIMIT,
            STR_PRODUCT_LIST_LOWER_LIMIT
        )

        # 5.- Total y método de pago
        found_total_line = lf.find_line_with_similarity(lines, STR_PRODUCT_LIST_LOWER_LIMIT)
        payment = self.find_payment_information(lines)

        if payment is None:
            raise Exception("Store not found")

        # 6.- Build ticket
        ticket_response["company"] = CompanySchema().dump(company)
        ticket_response["store"] = StoreSchema().dump(store)
        ticket_response["date"] = found_date.value_requested[0]
        ticket_response["lines"] = found_product_lines.value_requested
        ticket_response["payment"] = PaymentInformationSchema().dump(payment)
        print(json.dumps(ticket_response, indent=2, default=str, ensure_ascii=False))
        return ticket_response

mercadona_ticket_parser = MercadonaTicketParser()
mercadona_ticket_parser.parse(example_ticket)