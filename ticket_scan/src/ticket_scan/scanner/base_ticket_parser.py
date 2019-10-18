import os
import requests
from abc import ABC, abstractmethod

from ticket_scan.store.company_store import CompanyStore
from ticket_scan.store.store_store import StoreStore
from ticket_scan.model.company import CompanySchema
from ticket_scan.model.store import StoreSchema
from ticket_scan.scanner.slicer import SlicerOptions

DEFAULT_SIMILARITY_TH = 70

URL_TICKET_STORE = "http://localhost:5001"
END_POINT_COMPANIES = "get_companies"
END_POINT_STORES = "get_stores"


class BaseTicketParser(ABC):

    company_store = CompanyStore()
    store_store = StoreStore()

    def get_available_companies(self):
        return self.company_store.find_all()

    def get_available_stores(self, company_id=None):
        return self.store_store.find_all_with_company_id(company_id)

    @property
    @abstractmethod
    def company_name(self):
        pass

    @property
    @abstractmethod
    def company_tax_id(self):
        pass

    @property
    def slicer_options(self):
        return SlicerOptions()

    @abstractmethod
    def find_company(self, lines: list, available_companies: list, similarity_th=DEFAULT_SIMILARITY_TH):
        pass

    @abstractmethod
    def find_store(self, lines: list, available_stores: list, similarity_th=DEFAULT_SIMILARITY_TH):
        pass

    @abstractmethod
    def find_payment_information(self, lines: list):
        pass

    @abstractmethod
    def find_lines_address(self, lines: list, company: dict):
        pass

    @abstractmethod
    def parse(self, ticket: dict):
        pass

