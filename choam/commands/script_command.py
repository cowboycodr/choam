import os
import subprocess

from choam.constants import PYTHON_INTERPRETER, FOLDER_SEPERATOR

from choam.commands.command import Command

class ScriptCommand(Command):
    def __init__(
        self,
        choam
    ):
        super().__init__(ctx=choam)

        self.script_variables = {
            "PYTHON": PYTHON_INTERPRETER,
            "CWD": self.directory,
            "PROJECT": self.project_name,
            "SEP": FOLDER_SEPERATOR
        }

    def run(
        self,
        path_or_script: str,
        *args,
        **kwargs,
    ):
        '''
        Run a Choam script defined in `Choam.toml`
        or fun a file relative to `Choam.toml` with 
        the `--is-file` flag.

        Flags:
            `--description`: describes the script

            `--command`: shows the command that is going to execute

            `--perspective`: shows where the command will execute
        '''

        config = self.config.get()

        self.ctx._require_choam()
        if self.describe(path_or_script, **kwargs): return

        if "is_file" in kwargs.keys() or args:
            path = path_or_script

            if not path:
                subprocess.call(
                    [
                        PYTHON_INTERPRETER,
                        "-m",
                        self.project_name,
                        *args,
                    ]
                )

                return

            subprocess.call(
                [
                    PYTHON_INTERPRETER,
                    os.path.join(self.directory, self.project_name, path)
                ]
            )
            
            return

        script = path_or_script
        command_keys = config["script"][script].keys()

        if "perspective" in command_keys:
            perspective = config["script"][script]["perspective"]
            perspective = self.replace_with_script_vars(perspective)
        
        else:
            perspective = self.directory

        if "requires" in command_keys:
            requires = config["script"][script]["requires"]
        
        else:
            requires = []

        command = config["script"][script]["command"]
        command = self.replace_with_script_vars(command)

        for req in requires:
            self.ctx.add(
                dependency_name=req,
                install=True,
                dev=True
            )

        self.ctx._log(f"({perspective}) : {command}")
        os.system(f"cd {perspective} && {command}")

    def describe(self, script, **kwargs) -> bool:
        '''
        Describe the details of a script. Returns a bool depending 
        on whether or not it desciped a script

        Triggered when the use of the following flags
        occur:

            `--description`: Describes what the command does

            `--perspective`: Shows where the command is going to run

            `--command`: Shows the actual command that is going to run
        '''

        config = self.config.get()

        if kwargs.get("description", None):
            description_value = config["script"][script]["description"]

            self.ctx._log(f"(description) {script}: {description_value}")

            return True

        elif kwargs.get("perspective", None):
            perspective_value = config["script"][script]["perspective"]
            perspective_value = self.replace_with_script_vars(perspective_value)

            self.ctx._log(f"(perspective) {script}: {perspective_value}")

            return True

        elif kwargs.get("command" ,None):
            command_value = config["script"][script]["perspective"]
            command_value = self.replace_with_script_vars(command_value)

            self.ctx._log(f"(command) {script}: {command_value}")

            return True
        
        else:
            return False

    def replace_with_script_vars(self, string) -> str:
        result = string

        for name, value in self.script_variables.items():
            name = "${" + name + "}"

            result = result.replace(name, value)

        return result