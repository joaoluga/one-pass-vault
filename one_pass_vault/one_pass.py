from .command_builder.one_pass_command_builder import OnePassCommandBuilder
import os



class OnePass(OnePassCommandBuilder):

    def __init__(self):
        self.session_token = os.environ['ONE_PASS_VAULT_SESSION_TOKEN']

    def get_item(self, item_name):
        response = self.run_op_command(f"get item {item_name}", need_session=True)
        print(response) 
        return response
