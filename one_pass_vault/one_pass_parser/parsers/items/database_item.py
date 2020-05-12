from .item import Item

class DatabaseItem(Item):

    item_type = 'database'

    item_fields = ['database_type',
                   'hostname',
                   'port',
                   'database',
                   'username',
                   'password']

    def parse_response(self, response):
        parsed_response = {}
        dict_fields = response['details']['sections'][0]['fields']
        for field in dict_fields:
            if field['n'] in self.item_fields:
                parsed_response[field['n']] = field['v']
        return parsed_response
