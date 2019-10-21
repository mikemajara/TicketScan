from abc import ABC, abstractmethod

URL_TICKET_STORE = "http://localhost:5001"


class BaseStore(ABC):

    store_url = URL_TICKET_STORE
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_one(self, _id):
        pass
