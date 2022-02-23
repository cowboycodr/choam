import subprocess

from choam.constants import PYTHON_INTERPRETER
from choam.commands.command import Command

class PublishCommand(Command):
    '''
    Choam's command to publish current Choam project
    to https://pypi.org
    '''

    def __init__(self, choam):
        super().__init__(ctx=choam)

    def run(self):
        '''
        Publish current Choam project to https://pypi.org

        > Note: this method uses twin which will require
        your pypi credentials. Choam is no way affiliated
        twine and it is beyond our responsibility.
        '''
        self.ctx.add("twine", dev=True)
        self.ctx.add("wheel", dev=True)
        self.ctx.install()

        self.ctx._log(
            "Attempting real publication to https://pypi.org"
        )

        subprocess.call(
            [
                PYTHON_INTERPRETER,
                "setup.py",
                "sdist",
                "bdist_wheel"
            ]
        )

        subprocess.call(
            [
                PYTHON_INTERPRETER,
                "-m",
                "twine",
                "upload",
                "dist/*"
            ]
        )

        self.ctx._log("Real publication attempt completed")