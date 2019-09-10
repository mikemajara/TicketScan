class Store(object):
    def __init__(self,
                 company: str,
                 country: str,
                 city: str,
                 address: str,
                 phone: str,
                 id: str
                 ):
        self.company = company
        self.country = country
        self.city = city
        self.address = address
        self.phone = phone
        self.id = id

    @classmethod
    def from_json(cls, data):
        return cls(**data)