'''
Choam command-line interface entry point

Choam is a python project manager with the following capabilities:
- custom scripts
- dependencies
- configurations
- publication
'''

import os
import sys
import shutil
import subprocess
from typing import Optional

import fire
import pkg_resources
import toml

from choam.commands import *
from choam.constants import (FOLDER_SEPERATOR, OPERATING_SYSTEM,
                             PYTHON_INTERPRETER, SETUP_FILE_NAME)
from choam.create_setup_file import create_setup_file
from choam.find_dependencies import find_dependencies
from choam.folder_structure import FolderStructure as FS
from choam.gitignore import GITIGNORE
from choam.config_manager import ConfigManager


PROJECT_NAME = FS.get_project_name()

class Choam:
    '''
    Choam is a Python project manager designed for
    maanging dependencies, configurations and more.
    '''

    def __init__(self):
        self.configurations = ConfigManager()

    def _require_choam(self):
        if not FS.is_choam_project():
            Choam._log("Must be a choam project.")
            sys.exit()

    def _is_config_section(self, section_name: str) -> bool:
        if section_name in self.configurations.get().keys():
            return True

        return False

    def _add_config_section(self, section_name: str):
        new_config = self.configurations.get()
        new_config[section_name] = ""

        self.configirations.set(new_config)

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
        '''
        Choam's config command for reading/managing
        configurations from the command-line using Choam
        '''
        ConfigCommand(self).run(key, values)

    def init(self, adapt: Optional[bool] = None):
        '''
        Choam's initialize command for initializing
        a new Choam project inside the working 
        directory
        '''
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
        NewCommand(self).run(name)

    def _log_run_script(
        self,
        description,
        command,
        perspective,
        description_value,
        command_value,
        perspective_value,
    ):
        if description:
            self._log(description_value)

        elif command:
            self._log(command_value)

        elif perspective:
            self._log(perspective_value)

    def script(
        self,
        path_or_script: str = "",
        *args,
        **kwargs
    ):
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

    def _init_setup(self):
        directory = os.getcwd()

        config = self.configurations.get()

        package_config = config["package"]
        name = package_config["name"]
        version = package_config["version"]

        try:
            description = package_config["description"]
        except KeyError:
            description = ""

        try:
            repo_url = package_config["repo"]
        except KeyError:
            repo_url = ""

        modules = config["modules"]

        template = {
            f"{FOLDER_SEPERATOR}{SETUP_FILE_NAME}": create_setup_file(
                name,
                version,
                description,
                modules,
                repo_url,
            )
        }

        self._log_multiple(
            [
                f"Successfully setup '{name}' for PyPi publication",
                "Use '$ choam publish' when configurations have been set",
            ]
        )

        FS.construct_from_dict(template, f"{directory}{FOLDER_SEPERATOR}")

    def setup(self):
        """
        Configure `setup.py` according to `Choam.toml` while
        keeping all other configurations.

        If `setup.py` file does not exist then it will create
        it.

        Additional configurations may be done to `setup.py`
        after this command has been run.
        """

        if not FS.is_choam_project():
            self._log(f"{os.getcwd()}: not a Choam project.")

            return

        if not os.path.exists("setup.py"):
            self._init_setup()

            return

        config = self.configurations.get()
        new_setup_file = ""

        # Rewrite with `Choam.toml` configurations
        with open("./setup.py", "r", encoding="utf-8") as file:
            format_line = lambda l: "\t" + l + ",\n"

            for line in file.readlines():
                if line.strip().startswith("version"):
                    new_setup_file += format_line(
                        f'version="{config["package"]["version"]}"'
                    )

                elif line.strip().startswith("install_requires"):
                    modules = config["modules"]

                    new_setup_file += format_line(
                        f"install_requires={list(modules)}"
                    )

                else:
                    new_setup_file += line

        with open("setup.py", "w", encoding="utf-8") as file:
            file.write(new_setup_file)

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

        config = self.configurations.get()

        if ignore:
            config["modules-ignore"][dependency_name] = "*"

            if dependency_name in config["modules"].keys():
                config["modules"].pop(dependency_name)

            self.configurations.set(config)

            return

        if dev:
            if not self._is_config_section("modules-dev"):
                config["modules-dev"] = {}

            config["modules-dev"][dependency_name] = "*"

            if dependency_name in config["modules"]:
                config["modules"].pop(dependency_name)

        else:
            config["modules"][dependency_name] = "*"

        self.configurations.set(config)

        if install:
            self.install()

    def install(self, dep: Optional[str] = None):
        """
        Install all required dependencies from `Choam.toml`
        modules section.

        Args
            :dep: add depedency to required modules and install

            :find_deps: find project's required dependencies and install
            immediately
        """

        if dep:
            self.add(dep)

        config = self.configurations.get()

        if not self._is_config_section("modules-dev"):
            config["modules-dev"] = {}

        modules = {
            **config["modules"],
            **config["modules-dev"],
        }

        required_mods = set(modules)
        installed_mods = {mod.key for mod in set(pkg_resources.working_set)}
        missing_mods = required_mods - installed_mods

        for mod in missing_mods:
            self._log(f"Installing {mod}")

            module_string = (
                f"{mod}=={modules[mod]}"
                if modules[mod] != "*"
                else f"{mod}--upgrade"
            )
            upgrade_module = module_string.endswith("--upgrade")

            subprocess.call(
                [
                    PYTHON_INTERPRETER,
                    "-m",
                    "pip",
                    "install",
                    module_string.replace("--upgrade", ""),
                    "--upgrade" if upgrade_module else "",
                ]
            )

    def publish(self):
        """
        Publish package to https://PyPi.org following `Choam.toml` and `setup.py`
        configurations

        > Note: this method requires your https://PyPi.org credentials for twine
        to properly publish.

        Args:
            :setup_file_name: file to pull configurations from by default `setup.py`
        """

        self.add("twine")
        self.add("wheel")
        self.install()

        self._log(
            "Attempting real publication to https://test.pypi.org/legacy"
        )

        subprocess.call(
            [
                PYTHON_INTERPRETER,
                f"{SETUP_FILE_NAME}",
                "sdist",
                "bdist_wheel",
            ]
        )
        subprocess.call(
            [
                PYTHON_INTERPRETER,
                "-m",
                "twine",
                "upload",
                "dist/*",
            ]
        )

        self._log("Real publication attempt completed")

    def deps(self):
        """
        Automatically search project files for imported
        depedencies and add them to `Choam.toml` as well
        as setup
        """

        dependencies = find_dependencies()
        config = self.configurations.get()

        for dep in config["modules-ignore"]:
            if dep in config["modules"].keys():
                config["modules"].pop(dep)

        # Merging pre-existing dependencies with new found ones
        dep_config = {
            **config["modules"],
            **{dep: "*" for dep in dependencies},
        }

        # Sorting configurations by length
        config["modules"] = {
            key: dep_config[key] for key in sorted(dep_config, key=len)
        }

        self.configurations.set(config)

    def reqs(self):
        """
        Convert `Choam.toml` to `requirements.txt` accordingly
        """

        config = self.configurations.get()
        directory = os.getcwd()
        path = "requirements.txt"

        pip_versions_proc = subprocess.Popen(
            [PYTHON_INTERPRETER, "-m", "pip", "freeze"],
            stdout=subprocess.PIPE
        )

        pip_versions_string = str(pip_versions_proc.communicate()[0])
        pip_versions_proc.kill()

        pip_versions = {}

        for mod in pip_versions_string.split("\\n"):
            if mod.count("==") > 0:
                mod_name = mod.split("==")[0]
                mod_ver = mod.split("==")[1]
            elif mod.count("@"):
                mod_name = mod.split("@")[0].strip()
                mod_ver = mod.split("@")[1].strip()
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

        template = {path: requirements_content}

        if os.path.exists(path):
            self._log(
                f"{path}: Already exists. Either delete or rewrite requirements"
                " accordingly."
            )

        FS.construct_from_dict(template, directory)


def main():
    '''
    Choam main entrypoint for setup.py console scripts
    '''

    fire.Fire(Choam())


if __name__ == "__main__":
    main()
