from .command_builder import CommandBuilder


class OnePassCommandBuilder(CommandBuilder):

    __OP_CLI = "op"

    def __create_basic_command(self, details, need_session):
        # Create a basic op command to run
        result = [self.__OP_CLI]
        result.extend(details.split(" "))
        if need_session:
            result.append(f"--session={self.session_token}")
        return result

    def run_op_command(self, command_as_str, need_session=False,
                       json_output=True):
        # Given a string, simply run a op command
        return self.run_command(
                self.__create_basic_command(
                    command_as_str,
                    need_session=need_session
                ),
                json_output=json_output
            )
