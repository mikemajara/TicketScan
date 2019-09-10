from .store import Store
from .ticket_line import TicketLine
import datetime as dt
from typing import List

class Ticket(object):
    def __init__(self,
                 store: Store,
                 datetime: dt.datetime,
                 proprietaryTicketCodes: list,
                 paymentMethod: str,
                 total: float,
                 returned: float,
                 lines: List[TicketLine]):
        self.store = store
        self.datetime = datetime
        self.proprietaryTicketCodes = proprietaryTicketCodes
        self.paymentMethod = paymentMethod
        self.total = total
        self.returned = returned
        self.lines = lines

    @classmethod
    def from_json(cls, data):
        return cls(**data)