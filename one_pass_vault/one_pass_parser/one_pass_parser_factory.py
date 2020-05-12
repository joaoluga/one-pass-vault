from one_pass_vault.one_pass_parser.parsers.one_pass_item_parser import OnePassItemParser


class OnePassParserFactory:

    __PARSERS = {
        'item': OnePassItemParser()
    }

    def __init__(self, parser_type):
        self.__parser_type = parser_type

    def build_parser(self):
        return self.__PARSERS[self.__parser_type]
