from abc import ABC, abstractmethod


class Item(ABC):

    @property
    def item_type(self):
        return self.item_type

    def item_fields(self):
        return self.item_fields

    @abstractmethod
    def parse_response(self, response):
        pass
