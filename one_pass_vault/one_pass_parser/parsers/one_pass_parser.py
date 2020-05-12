from abc import ABC, abstractmethod
import os

class OnePassParser(ABC):

    @property
    def parser_type(self):
        return self.parser_type

    @abstractmethod
    def parse_response(self, response):
        pass
