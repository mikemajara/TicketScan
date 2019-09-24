import os
import requests
from abc import ABC, abstractmethod

DEFAULT_SIMILARITY_TH = 70

URL_TICKET_STORE = "http://localhost:5001"
END_POINT_COMPANIES = "get_companies"
END_POINT_STORES = "get_stores"


class BaseTicketParser(ABC):

    @staticmethod
    def get_available_companies():
        r = requests.get(os.path.join(URL_TICKET_STORE, END_POINT_COMPANIES))
        available_companies = r.json()
        return available_companies

    @staticmethod
    def get_available_stores(company_id):
        r = requests.get(os.path.join(URL_TICKET_STORE, END_POINT_STORES, company_id))
        available_stores = r.json()
        return available_stores

    @property
    @abstractmethod
    def company_name(self):
        pass

    @property
    @abstractmethod
    def company_tax_id(self):
        pass

    @abstractmethod
    def find_company(self, lines: list, available_companies: list, similarity_th=DEFAULT_SIMILARITY_TH):
        pass

    @abstractmethod
    def find_store(self, lines: list, available_stores: list, similarity_th=DEFAULT_SIMILARITY_TH):
        pass

    @abstractmethod
    def find_payment_method(self, lines: list):
        pass

    @abstractmethod
    def find_lines_address(self, lines: list, company: dict):
        pass

    @abstractmethod
    def parse(self, ticket: dict):
        pass

