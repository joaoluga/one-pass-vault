from .one_pass_parser import OnePassParser
from .items.application_item import ApplicationItem
from .items.database_item import DatabaseItem


class OnePassItemParser(OnePassParser):

    parser_type = 'item'

    __ITEM_TYPES = {
        'database': DatabaseItem(),
        'application': ApplicationItem()
    }

    def parse_response(self, response):

        item_type = self.__get_item_type(response)
        item = self.__ITEM_TYPES[item_type]
        return item.parse_response(response)

    def __get_item_type(self, response):

        try:
            return response['details']['sections'][1]['fields'][0]['v']
        except IndexError:
            return response['details']['sections'][0]['fields'][0]['v']
