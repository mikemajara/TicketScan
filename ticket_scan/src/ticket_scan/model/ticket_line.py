class TicketLine(object):
    def __init__(self,
            units: float,
            name: str,
            price: float,
            weight: str,
            weightPrice: float,
            readableName: str,
            id: str):
        self.units = units;
        self.name = name;
        self.price = price;
        self.weight = weight;
        self.weightPrice = weightPrice;
        self.readableName = readableName;
        self.id = id;

    @classmethod
    def from_json(cls, data):
        return cls(**data)