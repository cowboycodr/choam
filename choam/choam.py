"""
Choam command-line interface entry point

Choam is a python project manager with the following capabilities:
- custom scripts
- dependencies
- configurations
- publication
"""

import sys
from typing import Optional

import fire

from choam.commands import *
from choam.config_manager import ConfigManager
from choam.constants import OPERATING_SYSTEM
from choam.folder_structure import FolderStructure as FS


class Choam:
    """
    Choam is a Python project manager designed for
    maanging dependencies, configurations and more.
    """

    def __init__(self):
        self.configurations = ConfigManager()

    def _require_choam(self):
        if not FS.is_choam_project():
            self._log("Must be a choam project.")
            sys.exit()

    def _log(self, message: str):
        print(f"\n\t{message}")

        if OPERATING_SYSTEM != "windows":
            print()

    def _log_multiple(self, messages: list):
        print()
        for message in messages:
            print(f"\t{message}")

        if OPERATING_SYSTEM != "windows":
            print()

    def config(self, key: str, *values):
        """
        Choam's config command for reading/managing
        configurations from the command-line using Choam
        """
        ConfigCommand(self).run(key, *values)

    def init(self, adapt: Optional[bool] = None):
        """
        Choam's initialize command for initializing
        a new Choam project inside the working
        directory
        """
        InitCommand(self).run(adapt)

    def cleanup(self):
        """
        Remove build directories discharged from publication
        & attempts
        """
        CleanUpCommand(self).run()

    def new(self, name: str):
        """
        Initalize and generate a Choam project
        inside of a new directory
        """
        NewCommand(self).run(name=name)

    def script(self, path_or_script: str = "", *args, **kwargs):
        """
        Run a `Choam` script defined in `Choam.toml` or run project's default entry
        point or specify a relative filepath for Choam to run.

        Args:
            :path_or_script: specific filepath or script for `Choam` to run (default is script)

            :description: prints out the provided description of the command if there is one

            :command: prints out the command that will be run without actually running it
        """
        ScriptCommand(self).run(
            path_or_script,
            *args,
            **kwargs,
        )

    def setup(self):
        """
        Automatically configure `setup.py` according to `Choam.toml`
        """
        SetupCommand(self).run()

    def add(
        self,
        dependency_name: str,
        install: Optional[bool] = None,
        dev: Optional[bool] = None,
        ignore: Optional[bool] = None,
    ):
        """
        Add a required depedency to the depdency list
        """
        AddCommand(self).run(
            dependency_name=dependency_name,
            install=install,
            dev=dev,
            ignore=ignore,
        )

    def install(self, dep: Optional[str] = None):
        """
        Install all required dependencies according to
        `Choam.toml`

        Args
            :dep: add depedency to required modules and install
        """
        InstallCommand(self).run(dep)

    def publish(self):
        """
        Publish current Choam project to https://pypi.org

        > Note: this method uses twin which will require
        your pypi credentials. Choam is no way affiliated
        twine and it is beyond our responsibility.
        """
        PublishCommand(self).run()

    def deps(self):
        """
        Find dependencies and rewrite `Choam.toml`
        accordingly.
        """
        DepsCommand(self).run()

    def reqs(self):
        """
        Convert `Choam.toml` to `requirements.txt` accordingly
        """
        ReqsCommand(self).run()


def main():
    """
    Choam main entrypoint for setup.py console scripts
    """

    fire.Fire(Choam())


if __name__ == "__main__":
    main()
