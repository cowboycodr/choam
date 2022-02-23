import os
import shutil

from pathlib import Path
from typing import Optional

from choam.commands.command import Command
from choam.templates.gitignore import GITIGNORE
from choam.folder_structure import FolderStructure as FS

from choam.constants import (
    FOLDER_SEPERATOR
)

class InitCommand(Command):
    '''
    Choam's initialize command for initializing
    a new Choam project inside the working 
    directory
    '''

    def __init__(self, choam):
        super().__init__(ctx=choam)

    def run(
        self,
        adapt: Optional[bool] = None
    ):
        directory = self.directory
        name = self.project_name

        if FS.is_choam_project(directory):
            self.ctx._log("Already a choam project.")

            return

        if adapt:
            # TODO: Implement Initcommand@adapt method
            self.adapt(directory, name)

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

    def adapt(
        self
    ):
        '''
        Adapt a pre-existing project to Choam's standards
        '''

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
            item_name = item.split(FOLDER_SEPERATOR)[-1]

            if item_name in project_files:
                continue

            dest = FOLDER_SEPERATOR.join(*Path(item).parents, project_name, item_name)

            try:
                os.makedirs(
                    dest,
                    mode=0o666,
                    exist_ok=True
                ) 
            except OSError:
                self.ctx._log(f"(ignored) Error: Failed to make '{dest}'")

            do_move = input(
                f"Would you like to move: '{os.path.abspath(item_name)}'?"
                " (Y/n)"
            )

            if do_move == "" \
                    or do_move.lower().startswith("y"):
                
                try:
                    shutil.move(item_name, dest)
                except FileNotFoundError:
                    self.ctx._log(f"(ignored) Item not found: '{item_name}'")

        template = {
            f"{FOLDER_SEPERATOR}Choam.toml": (
                f'[package]\nname="{project_name}"\nversion="0.0.0"\n'
                f'description=""\nrepo="*required*"\nkeywords=[]'
                f'\n\n[modules-ignore]\n\n[modules]'
            ),
            f"{FOLDER_SEPERATOR}README.md": (
                f"{project_name}\n###This project was structure with"
                " [Choam](https://github.com/cowboycodr/choam)"
            ),
            f"{FOLDER_SEPERATOR}.gitignore": GITIGNORE,
        }

        FS.construct_from_dict(template, directory)
        self.ctx.deps()