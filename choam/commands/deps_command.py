"""
Choam's command for finding depedencies in the Choam
project and rewriting `Choam.toml` accordingly.
"""

from choam.commands.command import Command
from choam.find_dependencies import find_dependencies


class DepsCommand(Command):
    """
    Choam's command to find dependencies and
    rewrite `Choam.toml` accordingly
    """

    def __init__(self, choam):
        super().__init__(ctx=choam)

    def run(self):
        """
        Find dependencies and rewrite `Choam.toml` accordingly
        """

        config = self.config.get()
        dependencies = find_dependencies()

        for dep in config["modules-ignore"]:
            if dep in config["modules"].keys():
                config["modules"].pop(dep)

        # Merging already known imports with new
        # found imports
        dependencies = {**config["modules"], **{dep: "*" for dep in dependencies}}

        # Sorting configurations by length
        config["modules"] = {dependencies.items()}

        self.config.set(config)
