from marshmallow import Schema, fields, post_load
from typing import List


class StoreSchema(Schema):
    _id = fields.Integer()
    company_id = fields.Integer()
    country = fields.Str()
    city = fields.Str()
    address = fields.Str()
    address_strings = fields.List(fields.Str(), allow_none=True)
    phone = fields.Str(allow_none=True)

    @post_load
    def from_json(self, data, **kwargs):
        return Store(**data)


class Store(object):
    def __init__(self,
                 _id: int,
                 company_id: int,
                 country: str,
                 city: str,
                 address: str,
                 address_strings: List[str],
                 phone: str,
                 ):
        self._id = _id
        self.company_id = company_id
        self.country = country
        self.city = city
        self.address = address
        self.address_strings = address_strings
        self.phone = phone
