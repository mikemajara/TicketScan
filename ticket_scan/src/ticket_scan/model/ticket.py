from ticket_scan.model.store import Store, StoreSchema
from ticket_scan.model.company import Company, CompanySchema
from ticket_scan.model.payment_information import PaymentInformation, PaymentInformationSchema
from ticket_scan.model.ticket_line import TicketLine, TicketLineSchema
import datetime as dt
from typing import List
from marshmallow import Schema, fields, post_load, validate

VALID_DATE_FORMAT = "%d/%m/%Y %H:%M"
VALID_DATE_REGEX = "(\d{2}/\d{2}/\d{4}) *(\d{2}:\d{2})"

def format_ticket_date(date, hour):
    datetime_str = f"{date} {hour}"
    return dt.datetime.strptime(datetime_str, VALID_DATE_FORMAT)

class TicketSchema(Schema):
    id = fields.Str(allow_none=True)
    store = fields.Nested(StoreSchema, allow_none=True)
    company = fields.Nested(CompanySchema, allow_none=False)
    payment_information = fields.Nested(PaymentInformationSchema, allow_none=False)
    date = fields.DateTime(allow_none=False,
                           format=VALID_DATE_FORMAT)
    lines = fields.List(fields.Nested(TicketLineSchema))

    @post_load
    def from_json(self, data, **kwargs):
        return Ticket(**data)


class Ticket(object):
    def __init__(self,
                 _id: str = None,
                 store: Store = None,
                 company: Company = None,
                 payment_information: PaymentInformation = None,
                 datetime: dt.datetime = None,
                 lines: List[TicketLine] = []):
        self._id = _id
        self.store = store
        self.company = company
        self.payment_information = payment_information
        self.datetime = datetime
        self.lines = lines
