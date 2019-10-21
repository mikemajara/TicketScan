import os
import requests

from ticket_scan.model.store import StoreSchema
from ticket_scan.store.base_store import BaseStore

URL_FIND_ALL = "get_stores"
URL_FIND_ONE = "get_store"


class StoreStore(BaseStore):
    def find_all(self):
        response = requests.get(os.path.join(self.store_url, URL_FIND_ALL))
        result = response.json()
        return StoreSchema().load(result, many=True)

    def find_one(self, _id):
        response = requests.get(os.path.join(self.store_url, URL_FIND_ONE, _id))
        result = response.json()
        return StoreSchema().load(result)

    def find_all_with_company_id(self, company_id):
        response = requests.get(os.path.join(self.store_url, URL_FIND_ALL, company_id))
        result = response.json()
        return StoreSchema().load(result, many=True)

