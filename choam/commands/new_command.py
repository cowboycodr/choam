"""
Choam's command to initialize and generate a Choam
inside of a new directory
"""

from choam.commands.command import Command
from choam.constants import FOLDER_SEPERATOR
from choam.folder_structure import FolderStructure as FS
from choam.templates.gitignore import GITIGNORE


class NewCommand(Command):
    """
    Choam's command to initialize and generate a Choam project
    inside of a new directory
    """

    def __init__(self, choam):
        super().__init__(ctx=choam)

    def run(self, name: str):
        directory = self.directory
        folder_name = name

        # Choam project template
        template = {
            (
                f"{FOLDER_SEPERATOR}{folder_name}{FOLDER_SEPERATOR}"
                f"{folder_name}{FOLDER_SEPERATOR}__main__.py"
            ): (""),
            (
                f"{FOLDER_SEPERATOR}{folder_name}{FOLDER_SEPERATOR}"
                f"{folder_name}{FOLDER_SEPERATOR}__init__.py"
            ): "",
            f"{FOLDER_SEPERATOR}{folder_name}{FOLDER_SEPERATOR}Choam.toml": (
                f'[package]\nname = "{name}"\nversion = "0.0.1"\ndescription ='
                ' ""\n\n[modules]'
            ),
            f"{FOLDER_SEPERATOR}{folder_name}{FOLDER_SEPERATOR}README.md": (
                f"# {name}\n#### This project was constructed with"
                " [Choam](https://github.com/cowboycodr/choam)"
            ),
            f"{FOLDER_SEPERATOR}{folder_name}{FOLDER_SEPERATOR}.gitignore": GITIGNORE,
            f"{FOLDER_SEPERATOR}{folder_name}{FOLDER_SEPERATOR}setup.py": "",
        }

        print(template)
        FS.construct_from_dict(template, directory)
