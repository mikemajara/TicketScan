from marshmallow import Schema, fields, post_load, validates, validate, ValidationError

# ^ Should start with
# (www.)? may or may not have www.
# [a-z0-9]+(.[a-z]+) url and domain and also subdomain if any upto 2 levels
# (/[a-zA-Z0-9#]+/?)*/? can contain path to files but not necessary. last may contain a /
# $ should end there
VALID_URL_REGEX = "^(www.)?[a-z0-9]+\.[a-z]+(\/[a-zA-Z0-9#]+\/?)*$"

class CompanySchema(Schema):
    _id = fields.Str(required=True)
    name = fields.Str(required=True)
    tax_id = fields.Str(allow_none=True)
    web = fields.Str(allow_none=True,
                     validate=validate.Regexp(VALID_URL_REGEX))

    @post_load
    def from_json(self, data, **kwargs):
        return Company(**data)


class Company(object):
    def __init__(self,
                 _id: str,
                 name: str,
                 tax_id: str,
                 web: str = None
                 ):
        self._id = _id
        self.name = name
        self.tax_id = tax_id
        self.web = web

