"""
Generic command class for Choam's command-line-interface
"""

import os

from choam.message import Messenger
from choam.constants import OPERATING_SYSTEM
from choam.config_manager import ConfigManager
from choam.folder_structure import FolderStructure as FS


class Command:
    """
    Generic command class for Choam's command-line-interface
    """

    def __init__(
        self,
        ctx,
    ):
        self.ctx = ctx
        self.config = ConfigManager()
        self.messenger = Messenger()

        self.IS_WINDOWS = OPERATING_SYSTEM == "windows"

    def run(self):
        """
        Command code that will be executed goes here
        """

        pass

    @property
    def directory(self):
        return os.getcwd()

    @property
    def project_name(self):
        return FS.get_project_name()
