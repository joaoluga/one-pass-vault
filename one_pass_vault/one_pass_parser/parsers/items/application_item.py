from .item import Item

class ApplicationItem(Item):

    item_type = 'application'

    item_fields = ['username', 'password']

    def parse_response(self, response):

        parsed_response = {}
        dict_fields = response['details']['fields']
        for field in dict_fields:
            if field['name'] in self.item_fields:
                parsed_response[field['name']] = field['value']
        return parsed_response
