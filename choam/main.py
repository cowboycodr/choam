import os
import sys
import shutil
import pkg_resources
from typing import Optional

from choam.create_setup_file import create_setup_file
from choam.constants import (
    FOLDER_SEPERATOR,
    SETUP_FILE_NAME,
    PYTHON_INTERPRETER,
    OPERATING_SYSTEM,
)
from choam.find_dependencies import find_dependencies
from choam.folder_structure import FolderStructure as FS
from choam.gitignore import gitignore

import toml
import fire
import subprocess


class Choam:
    def __init__(self):
        pass

    def _get_config():
        with open(f"{os.getcwd()}/Choam.toml", "r") as f:
            return toml.loads(f.read())

    def _set_config(content: str):
        with open(f"{os.getcwd()}/Choam.toml", "w") as f:
            f.write(str(content))

    def _log(message: str):
        print(f"\n\t{message}")

        if OPERATING_SYSTEM != "windows":
            print()

    def _log_multiple(messages: "list[str]"):
        print()
        for message in messages:
            print(f"\t{message}")

        if OPERATING_SYSTEM != "windows":
            print()

    def config(self, key: str, *values):
        if len(values) == 0:
            return

        if len(values) == 1:
            values = values[0]

        config = Choam._get_config()

        config["package"][key] = values

        Choam._set_config(toml.dumps(config))

    def _adapt(self, directory: str, name: str):
        """
        Adapt an existing project directory to Choam's structure
        """

        PROJECT_FILES = [
            "requirements.txt",
            ".gitignore",
            "README.md",
            "README",
            "setup.py",
            "LICENSE.txt",
            ".git",
        ]

        for f in os.listdir(directory):
            file_name = f.split(FOLDER_SEPERATOR)[-1]
            dest = (
                os.path.abspath(
                    FOLDER_SEPERATOR.join(f.split(FOLDER_SEPERATOR)[:-1])
                    + FOLDER_SEPERATOR
                    + name
                    + FOLDER_SEPERATOR
                    + f.split(FOLDER_SEPERATOR)[-1]
                )
                .replace(FOLDER_SEPERATOR, "", 1)
                .replace(file_name, "", 1)
            )

            if file_name in PROJECT_FILES:
                continue

            try:
                os.makedirs(dest, mode=0o666, exist_ok=True)
            except:
                pass

            do_move = input(
                f"Would you like to move: {os.path.abspath(file_name)}? (Y/n) "
            )

            if do_move.lower().startswith("y"):
                try:
                    shutil.move(f, dest)
                except:
                    pass

        template = {
            f"{FOLDER_SEPERATOR}Choam.toml": f'[package]\nname="{name}"\nversion="0.0.0"\ndescription=""\nrepo="*required*"\nkeywords=[]\n\n[modules-ignore]\n\n[modules]',
            f"{FOLDER_SEPERATOR}README.md": f"{name}\n###This project was structure with [Choam](https://github.com/cowboycodr/choam)",
            f"{FOLDER_SEPERATOR}.gitignore": gitignore,
        }

        FS.construct_from_dict(template, directory)
        self.deps()

    def init(self, adapt: Optional[bool] = None):
        """
        Initalize a new Choam project in the working
        directory
        """

        directory = os.getcwd()
        name = directory.split(FOLDER_SEPERATOR)[-1]

        if FS.is_choam_project(directory):
            Choam._log("Already a Choam project.")
            return

        if adapt:
            self._adapt(directory, name)

            return

        template = {
            f"{directory}{FOLDER_SEPERATOR}{name}{FOLDER_SEPERATOR}__main__.py": "",
            f"{directory}{FOLDER_SEPERATOR}{name}{FOLDER_SEPERATOR}__init__.py": "__version__ == '0.1'",
            f"{directory}{FOLDER_SEPERATOR}Choam.toml": f'[package]\nname = "{name}\nversion = "0.0.1"\ndescription = ""\n\n[modules-ignore]\n\n[modules]',
            f"{directory}{FOLDER_SEPERATOR}README.md": f"# {name}\n#### This project was constructed with [Choam](https://github.com/cowboycodr/choam)",
            f"{directory}{FOLDER_SEPERATOR}.gitignore": gitignore,
            f"{directory}{FOLDER_SEPERATOR}setup.py": "",
            f"{directory}{FOLDER_SEPERATOR}setup.cfg": "# Custom configurations go here",
        }

        FS.construct_from_dict(template, directory)

    def cleanup(self):
        """
        Remove build directories discharged from `$ choam publish`
        """

        project_name = Choam._get_config()["package"]["name"]

        build_directories = ["build", f"{project_name}.egg-info", "dist"]

        if project_name in build_directories:
            Choam._log_multiple(
                [
                    "Cannot cleanup project that matches names with build directories list",
                    f"{project_name} is a reserved directory name.",
                ]
            )
            return

        for dirname in build_directories:
            path = f"{os.getcwd()}/{dirname}"

            if not os.path.exists(path):
                continue

            shutil.rmtree(path)

    def new(self, name: str):
        """
        Create a new directory and initalize a Choam project
        inside of it
        """

        directory = os.getcwd()

        folder_name = name.lower()

        # Choam project template
        template = {
            f"{FOLDER_SEPERATOR}{folder_name}{FOLDER_SEPERATOR}{folder_name}{FOLDER_SEPERATOR}__main__.py": "",
            f"{FOLDER_SEPERATOR}{folder_name}{FOLDER_SEPERATOR}{folder_name}{FOLDER_SEPERATOR}__init__.py": "__version__ == '0.1'",
            f"{FOLDER_SEPERATOR}{folder_name}{FOLDER_SEPERATOR}Choam.toml": f'[package]\nname = "{name}"\nversion = "0.0.1"\ndescription = ""\n\n[modules]\nchoam = "*"',
            f"{FOLDER_SEPERATOR}{folder_name}{FOLDER_SEPERATOR}README.md": f"# {name}\n#### This project was constructed with [Choam](https://github.com/cowboycodr/choam)",
            f"{FOLDER_SEPERATOR}{folder_name}{FOLDER_SEPERATOR}.gitignore": gitignore,
            f"{FOLDER_SEPERATOR}{folder_name}{FOLDER_SEPERATOR}setup.py": "",
            f"{FOLDER_SEPERATOR}{folder_name}{FOLDER_SEPERATOR}setup.cfg": "# Custom configurations go here",
        }

        FS.construct_from_dict(template, directory)

    def run(self, path_or_script: str, file: Optional[bool] = None, enable_script_variables: Optional[bool] = True, *args):
        """
        Run a `Choam` script defined in `Choam.toml` or run project's default entry 
        point or specify a relative filepath for Choam to run.

        :path_or_script: specific filepath or script for `Choam` to run (default is script)
        """

        if not FS.is_choam_project():
            Choam._log("Not a Choam project.")
            return

        config = Choam._get_config()
        project_folder = config['package']['name'].lower()

        if file:
            path = path_or_script

            if not path:
                subprocess.call([PYTHON_INTERPRETER, "-m", project_folder, *args])
                return

            subprocess.call(
                [
                    PYTHON_INTERPRETER,
                    os.path.join(os.getcwd(), project_folder, path),
                ]
            )
            return

        script = path_or_script
        current_dir = os.getcwd()
        perspective_folder = os.path.abspath(os.path.join(current_dir, config['script'][script]['perspective']))
        command = config['script'][script]['command']

        script_variables = {
            "PYTHON": PYTHON_INTERPRETER,
            "CWD": current_dir
        }

        if enable_script_variables:
            for var_name in script_variables.keys():
                command = command.replace("${" + var_name + "}", script_variables[var_name])

        Choam._log(command)

        os.system(f"cd {perspective_folder} && {command}")

    def _init_setup(self):
        directory = os.getcwd()

        config = Choam._get_config()

        package_config = config["package"]
        name = package_config["name"]
        version = package_config["version"]

        try:
            description = package_config["description"]
        except:
            description = ""

        try:
            repo_url = package_config["repo"]
        except:
            repo_url = ""

        try:
            keywords = package_config["keywords"]
        except:
            keywords = []

        modules = config["modules"]

        template = {
            f"{FOLDER_SEPERATOR}{SETUP_FILE_NAME}": create_setup_file(
                name, version, description, keywords, modules, repo_url
            )
        }

        Choam._log_multiple(
            [
                f"Successfully setup '{name}' for PyPi publication",
                f"Use '$ choam publish' when configurations have been set",
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
            Choam._log(f"{os.getcwd()}: not a Choam project.")

            return

        if not os.path.exists("setup.py"):
            self._init_setup()

            return

        config = Choam._get_config()
        new_setup_file = ""

        # Rewrite with `Choam.toml` configurations
        with open("./setup.py", "r") as f:
            format_line = lambda l: "\t" + l + ",\n"

            for line in f.readlines():
                if line.strip().startswith("version"):
                    new_setup_file += format_line(
                        f'version="{config["package"]["version"]}"'
                    )

                elif line.strip().startswith("install_requires"):
                    modules = config["modules"]

                    new_setup_file += format_line(
                        f"install_requires={[mod for mod in modules]}"
                    )

                else:
                    new_setup_file += line

        with open("setup.py", "w") as f:
            f.write(new_setup_file)

    def add(
        self,
        dependency_name: str,
        install: Optional[bool] = None,
        ignore: Optional[bool] = None,
    ):
        """
        Add a required depedency to the depdency list
        """

        config = Choam._get_config()

        if ignore:
            config["modules-ignore"][dependency_name] = "*"
            config["modules"].pop(dependency_name)

            Choam._set_config(toml.dumps(config))

            return

        config["modules"][dependency_name] = "*"

        Choam._set_config(toml.dumps(config))

        if install:
            self.install(find_dependencies=False)

    def install(self, dep: Optional[str] = None, find_deps: Optional[bool] = None):
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

        if find_deps:
            self.deps()

        config = Choam._get_config()

        required_mods = {mod for mod in config["modules"]}
        installed_mods = {mod.key for mod in pkg_resources.working_set}
        missing_mods = required_mods - installed_mods

        # Key: Module name, Value: Module version
        mod_ver = config["modules"]

        for mod in missing_mods:
            Choam._log(f"Installing {mod}")

            module_string = (
                f"{mod}=={mod_ver[mod]}" if mod_ver[mod] != "*" else f"{mod}--upgrade"
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
        Publish package to https://PyPi.org following `_file_name.py` and `setup.cfg`
        configurations

        > Note: this method requires your https://PyPi.org credentials for twine
        to properly publish.

        Args:
            :setup_file_name: file to pull configurations from by default `setup.py`
        """

        self.add("twine")
        self.add("wheel")
        self.install()

        Choam._log("Attempting real publication to https://test.pypi.org/legacy")

        subprocess.call(
            [PYTHON_INTERPRETER, f"{SETUP_FILE_NAME}", "sdist", "bdist_wheel"]
        )
        subprocess.call([PYTHON_INTERPRETER, "-m", "twine", "upload", "dist/*"])

        Choam._log("Real publication attempt completed")

    def deps(self):
        """
        Automatically search project files for imported
        depedencies and add them to `Choam.toml` as well
        as setup
        """

        dependencies = find_dependencies()
        config = Choam._get_config()

        for dep in config["modules-ignore"]:
            if dep in config["modules"].keys():
                config["modules"].pop(dep)

        # Merging pre-existing dependencies with new found ones
        dep_config = {**config["modules"], **{dep: "*" for dep in dependencies}}

        # Sorting configurations by length
        config["modules"] = {
            key: dep_config[key] for key in sorted(dep_config, key=len)
        }

        Choam._set_config(toml.dumps(config))

    def reqs(self):
        """
        Convert `Choam.toml` to `requirements.txt` accordingly
        """

        config = Choam._get_config()
        directory = os.getcwd()
        path = f"requirements.txt"

        pip_versions_proc = subprocess.Popen([PYTHON_INTERPRETER, "-m", "pip", "freeze"], stdout=subprocess.PIPE)
        pip_versions_string = str(pip_versions_proc.communicate()[0])
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

        requirements_content = ''
        for mod in config['modules']:
            mod_name = mod
            mod_ver = config['modules'][mod_name]

            if mod_ver == "*":
                try:
                    mod_ver = pip_versions[mod_name]
                except:
                    continue

            requirements_content += f'{mod_name}=={mod_ver}\n'

        template = {
            path: requirements_content
        }

        if os.path.exists(path):
            Choam._log(f"{path}: Already exists. Either delete or rewrite requirements accordingly.")

        FS.construct_from_dict(template, directory)


def main():
    fire.Fire(Choam())