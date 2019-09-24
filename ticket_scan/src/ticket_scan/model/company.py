from marshmallow import Schema, fields, post_load


class CompanySchema(Schema):
    _id = fields.Str()
    name = fields.Str()
    taxId = fields.Str()
    web = fields.Str(allow_none=True)

    @post_load
    def from_json(self, data, **kwargs):
        return Company(**data)


class Company():
    _id = fields.Str()
    name = fields.Str()
    taxId = fields.Str()
    web = fields.Str(allow_none=True)

    def __init__(self,
                 _id: str,
                 name: str,
                 taxId: str,
                 web: str = None
                 ):
        self._id = _id
        self.name = name
        self.taxId = taxId
        self.web = web

