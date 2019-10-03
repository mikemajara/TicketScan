import json

from ticket_scan.model.ticket import TicketSchema
from ticket_scan.model import Ticket
from ticket_scan.model.company import Company, CompanySchema
from ticket_scan.model.store import StoreSchema
from ticket_scan.model.payment_information import PaymentInformation, METHOD_CARD, METHOD_CASH, PaymentInformationSchema

from ticket_scan.scanner import line_finder as lf
from ticket_scan.scanner.base_ticket_parser import BaseTicketParser

import logging

from ticket_scan.scanner.slicer import SlicerOptions

DEFAULT_SIMILARITY_TH = 70

# TICKET LINE REFERENCES
STR_COMPANY_NAME = "LIDL SUPERMERCADOS S.A.U."
STR_COMPANY_TAX_ID = "NIF: A60195278"
STR_PRODUCT_LIST_UPPER_LIMIT = "Un"
STR_PRODUCT_LIST_LOWER_LIMIT = "—.—.————"
STR_TOTAL = "Total "
STR_CARD = "??? " # TODO: No info about how a card payment looks like
STR_CASH = "Entregado "

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
## not guaranteed to be a rightful value).

example_ticket = {
    "0": "LIDL SUPERMERCADOS S.A.U.",
    "1": "Avenida 'iiguel de Cervantes N9 110",
    "2": "30100 Murcia",
    "3": "NIF A60195278",
    "4": "www, lidl.es",
    "5": "Yogur griego 1,258",
    "6": "Danone activia 1,898",
    "7": "Gullón digestive 1,298",
    "8": "Yogur griego miel 0,49 B",
    "9": "Tortilla cebolla 0,79",
    "10": "III:",
    "11": "Entregado 20,21",
    "12": "Cambio -14,50",
    "13": "IVAX IVA + Preto = PV",
    "14": "B 10% 0,52 5,19 5,71",
    "15": ".—e—————— ——— o —————————— —); — —— — ————i—]]—]—",
    "16": "Suma 0,52 5,19 5,71",
    "17": "| Registrate en Lid! Plus y ahorra 1",
    "18": "1 en tus próximas compras 1",
    "19": "3508 214740/05 02.09.19 20:21",
    "20": "Devoluciones artículos de bazar con",
    "21": "ticket de compra y embalaje original",
    "22": "en un plazo máximo de 30 días sin",
    "23": "perjuicio de la ley de garantías.",
    "24": "Horario Tienda Lu a Sa 09:00 a 22:00",
    "25": "Atención al cliente",
    "26": "www. lid].es/contacto Tel,900958311",
    "27": "GRACIAS POR SU VISITA"
}

logger = logging.getLogger(__name__)


class LidlTicketParser(BaseTicketParser):
    @property
    def company_name(self):
        return STR_COMPANY_NAME

    @property
    def company_tax_id(self):
        return STR_COMPANY_TAX_ID

    @property
    def slicer_options(self):
        return SlicerOptions(cut_margin_factor=1.2)

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
    ## - [x] Make address a variable number of lines.
    ## for the moment in list all must be equal or higher to choose
    ## a another store.
    ## Addresses must be also filled in for the stores in the database
    ## - [ ] How should the method be tested? Test it!
    def find_store(self, address_lines: list, available_stores: list, similarity_th=DEFAULT_SIMILARITY_TH):
        result = None
        best_ratios = [0] * len(address_lines)

        for store in available_stores:
            ratios = [0] * len(store.address_strings)
            for idx, string in enumerate(store.address_strings):
                found_string = lf.find_line_with_similarity(address_lines, string)
                if found_string.is_found[0]:
                    ratios[idx] = found_string.ratio[0]
            if len(ratios) and all([r > br for r, br in zip(ratios, best_ratios)]):
                result = store
        return result

    def find_payment_information(self, lines: list):
        result = PaymentInformation()

        found_total = lf.find_line_with_similarity(lines, STR_TOTAL)
        if found_total.is_found[0]:
            result.total = found_total.value_requested[0].split(" ")[-1]

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
        # Lidl proprietary
        return lf.find_lines_with_limit(lines, company.name, amount_lines=2, limit_type="upper")

    def find_date(self, lines: list):
        date = None
        STR_LAST_LINE = "GRACIAS POR SU VISITA"
        NUM_LINES_UPWARD = 8
        found_timestamp = lf.find_lines_with_limit(lines, limit=STR_LAST_LINE, amount_lines=NUM_LINES_UPWARD, limit_type="lower")
        if found_timestamp.is_found:
            _, _, date, hour = found_timestamp.value_requested[0].split(" ")
        return date

    def parse(self, ticket: dict):
        ticket_response = {}
        company = None
        store = None
        lines = list(ticket.values())
        logger.info(json.dumps(lines, indent=2, default=str, ensure_ascii=False))

        # 1.- Find company
        company = self.find_company(
            lines,
            self.get_available_companies()
        )
        # company = next(filter(lambda x: found_company.value_requested[0] == x["name"], available_companies), None)
        # company = found_company.value_requested if found_company.is_found[0] else None

        if company is None or not isinstance(company, Company):
            raise Exception("Company not found")

        # 2.- Find store
        available_stores = self.get_available_stores(company._id)
        found_address_lines = self.find_lines_address(lines, company)
        store = self.find_store(found_address_lines.value_requested, available_stores)

        if store is None:
            raise Exception("Store not found")

        # 3.- Fecha
        found_date = self.find_date(lines)

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
        ticket_object = Ticket(
            company=company,
            store=store,
        )
        ticket_response["company"] = CompanySchema().dump(company)
        ticket_response["store"] = StoreSchema().dump(store)
        ticket_response["date"] = found_date
        ticket_response["lines"] = found_product_lines.value_requested
        ticket_response["payment"] = PaymentInformationSchema().dump(payment)
        logger.info(json.dumps(TicketSchema().dump(ticket), indent=2, default=str, ensure_ascii=False))
        return ticket_response


# mercadona_ticket_parser = MercadonaTicketParser()
# mercadona_ticket_parser.parse(example_ticket)