from subprocess import run, PIPE
import json


class CommandBuilder:

    def run_command(self, command, json_output=True):

        execution = run(
            command,
            stdout=PIPE,
            stderr=PIPE
        )

        result = execution.stdout.decode('UTF-8').replace('\n', '')
        if json_output:
            return json.loads(result)
        else:
            return result
