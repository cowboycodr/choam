import os
import subprocess

from choam.constants import PYTHON_INTERPRETER
from choam.commands.command import Command

class ReqsCommand(Command):
    '''
    Choam's command for converting `Choam.toml` requirements
    to `requirements.txt`.
    '''

    def __init__(
        self,
        choam
    ):
        super().__init__(ctx=choam)

    def run(self):
        '''
        Convert `Choam.toml` requirements to `requirements.txt` accordingly
        '''

        config = self.config.get()
        directory = self.directory

        path = os.path.join(directory, "requirements.txt")

        pip_versions_proc = subprocess.Popen(
            [
                PYTHON_INTERPRETER,
                "-m",
                "pip",
                "freeze"
            ],
            stdout=subprocess.PIPE
        )

        pip_versions_string = str(pip_versions_proc.communicate()[0])
        pip_versions_proc.kill()

        pip_versions = {}

        for mod in pip_versions_string.split("\\n"):
            if mod.count("==") == 1:
                mod_name = mod.split("==")[0]
                mod_ver = mod.split("==")[1]
            
            elif mod.count("@"):
                mod_name = mod.split("@")[0]
                mod_ver = mod.split("@")[1]

            else:
                continue

            pip_versions[mod_name] = mod_ver

        requirements_content = ""
        for mod in config["modules"]:
            mod_name = mod
            mod_ver = config["modules"][mod_name]

            if mod_ver == "*":
                try:
                    mod_ver = pip_versions[mod_name]
                except KeyError:
                    continue

            requirements_content += f"{mod_name}=={mod_ver}\n"

        with open(path, "w") as requirements:
            requirements.write(requirements_content)