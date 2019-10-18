from marshmallow import Schema, fields, post_load
from typing import Optional

class TicketLineSchema(Schema):
    _id = fields.Str(allow_none=True)
    units = fields.Integer()
    name = fields.Str()
    price = fields.Float()
    weight = fields.Float()
    weight_price = fields.Float()
    readable_name = fields.Str(allow_none=True)

    @post_load
    def from_json(self, data, **kwargs):
        return TicketLine(**data)


class TicketLine(object):
    def __init__(self,
                 _id: Optional[str] = None,
                 units: int = None,
                 name: str = None,
                 price: Optional[float] = None,
                 weight: Optional[float] = None,
                 weight_price: Optional[float] = None,
                 readable_name: Optional[str] = None,
                 ):
        self._id = _id
        self.units = units
        self.name = name
        self.price = price
        self.weight = weight
        self.weightPrice = weight_price
        self.readable_name = readable_name
