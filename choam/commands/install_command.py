"""
Choam's command to install required dependencies
from `Choam.toml`
"""

import os
from typing import Optional

import pkg_resources

from choam.commands.command import Command
from choam.constants import PYTHON_INTERPRETER


class InstallCommand(Command):
    """
    Install all require dependencies from `Choam.toml`
    """

    def __init__(
        self,
        choam,
    ):
        super().__init__(ctx=choam)

    def run(self, dep: Optional[str]):
        """
        Install all required dependencies according to
        `Choam.toml`

        Args:
            :dep: add and install depedency to required modules
        """

        if dep:
            self.ctx.add(dep)

        config = self.config.get()

        if not self.config.is_section("modules-dev"):
            config["modules-dev"] = {}

        modules = {**config["modules"], **config["modules-dev"]}

        required_mods = set(modules)
        installed_mods = {mod.key for mod in set(pkg_resources.working_set)}
        missing_mods = required_mods - installed_mods

        for mod in missing_mods:
            self.messenger.log(f"Installing {mod}")

            module_string = (
                f"{mod}=={modules[mod]}" if modules[mod] != "*" else f"{mod}--upgrade"
            )

            upgrade_module = module_string.endswith("--upgrade")
            module_string = module_string.replace("--upgrade", "")

            os.system(
                " ".join(
                    [
                        PYTHON_INTERPRETER,
                        "-m",
                        "pip",
                        "install",
                        module_string.replace,
                        "--upgrade" if upgrade_module else "",
                    ]
                )
            )
