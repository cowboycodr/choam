"""
Choam's command to initialize a new project
in the current directory.

Initialize a brand new project or adapt a 
pre-existing project to Choam's standards
"""

import os
import shutil
from typing import Optional

from choam.commands.command import Command
from choam.constants import FOLDER_SEPERATOR
from choam.folder_structure import FolderStructure as FS
from choam.templates.gitignore import GITIGNORE


class InitCommand(Command):
    """
    Choam's initialize command for initializing
    a new Choam project inside the working
    directory
    """

    def __init__(self, choam):
        super().__init__(ctx=choam)

    def run(self, adapt: Optional[bool] = None):
        directory = self.directory
        name = self.project_name

        if FS.is_choam_project(directory):
            self.messenger.log("Already a choam project.", self.messenger.types.WARNING)

            return

        if adapt:
            # TODO: Implement Initcommand@adapt method
            self.adapt()

            return

        template = {
            f"{FOLDER_SEPERATOR}{name}{FOLDER_SEPERATOR}__main__.py": "",
            f"{FOLDER_SEPERATOR}{name}{FOLDER_SEPERATOR}__init__.py": (
                "__version__ == '0.1'"
            ),
            f"{FOLDER_SEPERATOR}Choam.toml": (
                f'[package]\nname = "{name}"\nversion = "0.0.1"\ndescription ='
                ' ""\n\n[modules-ignore]\n\n[modules]'
            ),
            f"{FOLDER_SEPERATOR}README.md": (
                f"# {name}\n#### This project was constructed with"
                " [Choam](https://github.com/cowboycodr/choam)"
            ),
            f"{FOLDER_SEPERATOR}.gitignore": GITIGNORE,
            f"{FOLDER_SEPERATOR}setup.py": "",
        }

        FS.construct_from_dict(template, directory)

    def adapt(self):
        """
        Adapt a pre-existing project to Choam's standards
        """

        project_name = self.project_name
        directory = self.directory
        project_name = self.project_name

        project_files = [
            "requirements.txt",
            ".gitignore",
            "README.md",
            "README",
            "setup.py",
            "LICENSE.txt",
            ".git",
            ".choam",
            project_name,
        ]

        for item in os.listdir(directory):
            if os.path.isdir(item):
                continue

            item_name = item.split(FOLDER_SEPERATOR)[-1]

            if item_name in project_files:
                continue

            dest = (
                os.path.abspath(
                    FOLDER_SEPERATOR.join(item.split(FOLDER_SEPERATOR)[:-1])
                    + FOLDER_SEPERATOR
                    + project_name
                    + FOLDER_SEPERATOR
                    + item_name
                )
                .replace(FOLDER_SEPERATOR, "", 1)
                .replace(item_name, "", 1)
            )

            try:
                os.makedirs(dest, mode=0o777, exist_ok=True)
            except OSError:
                self.messenger.log(f"(ignored) Error: Failed to make '{dest}'")

            do_move = input(
                f"Would you like to move: '{os.path.abspath(item_name)}'?" " (Y/n)"
            )

            if do_move == "" or do_move.lower().startswith("y"):

                try:
                    shutil.move(item, dest)
                except FileNotFoundError:
                    self.messenger.log(f"(ignored) Item not found: '{item_name}'")
                except PermissionError:
                    self.messenger.log(
                        "(fatal) Unable to adapt directory files due to system permissions."
                    )
                    break

        template = {
            f"{FOLDER_SEPERATOR}Choam.toml": (
                f'[package]\nname="{project_name}"\nversion="0.0.0"\n'
                f'description=""\nrepo="*required*"\nkeywords=[]'
                f"\n\n[modules-ignore]\n\n[modules]"
            ),
            f"{FOLDER_SEPERATOR}README.md": (
                f"{project_name}\n###This project was structure with"
                " [Choam](https://github.com/cowboycodr/choam)"
            ),
            f"{FOLDER_SEPERATOR}.gitignore": GITIGNORE,
        }

        FS.construct_from_dict(template, directory)
        self.ctx.deps()
