"""
Choam's command to automaitcally configure `setup.py`
according to `Choam.toml`
"""

import os
from typing import Optional

from choam.commands.command import Command
from choam.constants import FOLDER_SEPERATOR
from choam.create_setup_file import create_setup_file


class SetupCommand(Command):
    """
    Choam's command to automatically configure `setup.py`
    according to `Choam.toml`
    """

    def __init__(self, choam):
        super().__init__(ctx=choam)

    def run(self):
        """
        Automaitcally configure `setup.py` according to `Choam.toml`
        """
        self.ctx._require_choam()

        config = self.config.get()
        setup_path = os.path.abspath(f"{self.directory}{FOLDER_SEPERATOR}setup.py")

        if not os.path.exists(setup_path):
            self.create_setup_file(setup_path)

            return

        new_setup_file = ""

        # Rewrite with `Choam.toml` configurations
        with open(setup_path, "r", encoding="utf-8") as file:
            format_line = lambda l: "\t" + l + ",\n"

            for line in file.readlines():
                if line.strip().startswith("version"):
                    new_setup_file += format_line(
                        f'version="{config["package"]["version"]}"'
                    )

                elif line.strip().startswith("install_requires"):
                    modules = config["modules"]

                    new_setup_file += format_line(f"install_requires={list(modules)}")

                else:
                    new_setup_file += line

        with open(setup_path, "w", encoding="utf8") as file:
            file.write(new_setup_file)

        self.messenger.log(f"Successfully configured '{self.project_name}' for publication")

    def create_setup_file(self):
        setup_path = os.path.abspath(f"{self.directory}{FOLDER_SEPERATOR}setup.py")

        config = self.config.get()
        package_config = config["package"]

        # List of possible config package items
        package_items = ["name", "version", "description", "repo", "modules"]

        package_info = {}

        for key in package_items:
            if key not in package_config.keys():
                package_info[key] = package_config[key]

        setup_content = create_setup_file(
            name=package_info["name"],
            version=package_info["version"],
            description=package_info["description"],
            modules=package_info["modules"],
            repo_url=package_info["repo_url"],
        )

        with open(setup_path, "w") as setup_file:
            setup_file.write(setup_content)

        self.ctx_log_multiple(
            [
                f"Successfully created '{self.project_name}' configurations for pypi publication",
                "Use `$ choam publish` when configurations have been set",
            ]
        )
