from marshmallow import Schema, fields, post_load, validate, ValidationError

METHOD_CARD = "CARD"
METHOD_CASH = "CASH"


class PaymentInformationSchema(Schema):
    total = fields.Float(required=True)
    method = fields.Str(required=True,
                        validate=validate.OneOf([METHOD_CARD, METHOD_CASH]))
    # ToDo: Do we really need returned?
    returned = fields.Str(allow_none=True)

    @validate("total")
    def validate_total(self, value):
        if value < 0:
            raise ValidationError("Total amount must be greater than 0")

    @post_load
    def from_json(self, data, **kwargs):
        return PaymentInformation(**data)


class PaymentInformation(object):
    def __init__(self,
                 total: str = None,
                 method: str = None,
                 returned: str = None,
                 ):
        self.total = total
        self.method = method
        self.returned = returned

