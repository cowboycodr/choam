"""
Choam's publish command for simple access to
publishing the current Choam project to https://pypi.org
"""

import subprocess
from typing import Optional

from choam.commands.command import Command
from choam.constants import PYTHON_INTERPRETER


class PublishCommand(Command):
    """
    Choam's command to publish current Choam project
    to https://pypi.org
    """

    def __init__(self, choam):
        super().__init__(ctx=choam)

    def run(
        self,
        quiet: Optional[bool] = None
    ):
        """
        Publish current Choam project to https://pypi.org

        > Note: this method uses twin which will require
        your pypi credentials. Choam is no way affiliated
        twine and it is beyond our responsibility.
        """
        self.ctx.add("twine", dev=True)
        self.ctx.add("wheel", dev=True)
        self.ctx.install()


        if quiet:
            out = subprocess.PIPE
        else:
            out = None

        with self.messenger.session() as messenger:

            messenger.log("Attempting real publication to https://pypi.org", _type=messenger.types.WARNING)
            messenger.newline()

            subprocess.Popen(
                [
                    PYTHON_INTERPRETER,
                    "setup.py",
                    "sdist",
                    "bdist_wheel"
                ],
                stdout=out
            ).wait(10)

            messenger.newline()
            messenger.log("Build completed.", _type=messenger.types.GOOD)
            messenger.newline()

            subprocess.Popen(
                [
                    PYTHON_INTERPRETER,
                    "-m",
                    "twine",
                    "upload",
                    "dist/*"
                ],
            ).wait()

            messenger.newine()
            messenger.log("Real publication attempt completed", _type=messenger.types.WARNING)
            messenger.newline()