from marshmallow import Schema, fields, post_load


class TicketLineSchema(Schema):
    _id = fields.Str()
    units = fields.Float()
    name = fields.Str()
    price = fields.Float()
    weight = fields.Float()
    weight_price = fields.Float()
    readable_name = fields.Str()

    @post_load
    def from_json(self, data, **kwargs):
        return TicketLine(**data)


class TicketLine(object):
    def __init__(self,
                 _id: str,
                 units: float,
                 name: str,
                 price: float,
                 weight: float,
                 weight_price: float,
                 readable_name: str,
                 ):
        self._id = _id
        self.units = units
        self.name = name
        self.price = price
        self.weight = weight
        self.weightPrice = weight_price
        self.readable_name = readable_name
