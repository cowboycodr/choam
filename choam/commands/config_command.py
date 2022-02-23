"""
Choam's config command for reading/managing 
configurations from the command-line
using Choam
"""

from choam.commands.command import Command


class ConfigCommand(Command):
    """
    Choam's config command for reading/managing
    configurations from the command-line using
    Choam
    """

    def __init__(
        self,
        choam,
    ):
        super().__init__(ctx=choam)

    def run(self, key: str, *values):
        config = self.config.get()

        if len(values) == 0:
            if key in config["package"].keys():
                value = config["package"][key]

                self.ctx._log(f"{key}: {value}")

            return

        if len(values) == 1:
            values = values[0]

        config["package"][key] = values

        self.config.set(config)
