from marshmallow import Schema, fields, post_load

METHOD_CARD = "CARD"
METHOD_CASH = "CASH"

# TODO
## - [ ] Validate that method is always one of the
## available values. Check also enum
## - [ ] The values total and returned must at some
## point be floats here.

class PaymentInformationSchema(Schema):
    total = fields.Str()
    method = fields.Str()
    returned = fields.Str(allow_none=True)

    @post_load
    def from_json(self, data):
        return PaymentInformation(**data)


class PaymentInformation():
    total = fields.Str(allow_none=True)
    method = fields.Str(allow_none=True)
    returned = fields.Str(allow_none=True)

    def __init__(self,
                 total: str = None,
                 method: str = None,
                 returned: str = None,
                 ):
        self.total = total
        self.method = method
        self.returned = returned

