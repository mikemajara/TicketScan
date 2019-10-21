import os
import requests
from abc import ABC, abstractmethod

from ticket_scan.model.ticket import Ticket, TicketSchema
from ticket_scan.store.base_store import BaseStore

URL_FIND_ALL = "get_all_tickets"
URL_FIND_ONE = "get_ticket"
URL_CREATE = "add_ticket"


class TicketStore(BaseStore):
    def find_all(self):
        response = requests.get(os.path.join(self.store_url, URL_FIND_ALL))
        result = response.json()
        return TicketSchema().load(result, many=True)

    def find_one(self, _id):
        response = requests.get(os.path.join(self.store_url, URL_FIND_ONE, _id))
        result = response.json()
        return TicketSchema().load(result)

    def create(self, ticket: Ticket):
        response = requests.post(
            os.path.join(self.store_url, URL_CREATE),
            None,
            ticket,
        )
        return response

