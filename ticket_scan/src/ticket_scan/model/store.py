from marshmallow import Schema, fields, post_load


class StoreSchema(Schema):
    _id = fields.Str()
    address = fields.Str()
    city = fields.Str()
    company_id = fields.Str()
    country = fields.Str()
    phone = fields.Str(allow_none=True)

    @post_load
    @post_load
    def from_json(self, data, **kwargs):
        return Store(**data)


class Store():
    def __init__(self,
                 _id: str,
                 company_id: str,
                 country: str,
                 city: str,
                 address: str,
                 phone: str,
                 ):
        self._id = _id
        self.address = address
        self.city = city
        self.company_id = company_id
        self.country = country
        self.phone = phone