"""
Choam command to cleanup build directoris discharged from
publication
"""

import os
import shutil

from choam.commands.command import Command


class CleanUpCommand(Command):
    """
    Choam's command to remove build directories discharged
    from publication & attempts
    """

    def __init__(self, choam):
        super().__init__(ctx=choam)

    def run(self):
        project_name = self.project_name

        build_directories = [
            "build",
            f"{project_name}.egg-info",
            "dist",
        ]

        if project_name in build_directories:
            self.ctx._log_multiple(
                [
                    "Cannot clean up project that matches named with"
                    " item in build directories list.",
                    f"{project_name} is a reserved build directory name.",
                ]
            )

            return

        for _dir in build_directories:
            path = f"{self.directory}/{_dir}"

            if not os.path.exists(path):
                continue

            shutil.rmtree(path)
