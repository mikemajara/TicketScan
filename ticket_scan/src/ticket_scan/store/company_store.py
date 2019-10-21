import os
import requests
from abc import ABC, abstractmethod

from ticket_scan.model.company import CompanySchema
from ticket_scan.store.base_store import BaseStore

URL_FIND_ALL = "get_companies"
URL_FIND_ONE = "get_company"


class CompanyStore(BaseStore):
    def find_all(self):
        response = requests.get(os.path.join(self.store_url, URL_FIND_ALL))
        result = response.json()
        return CompanySchema().load(result, many=True)

    def find_one(self, _id):
        response = requests.get(os.path.join(self.store_url, URL_FIND_ONE, _id))
        result = response.json()
        return CompanySchema().load(result)
