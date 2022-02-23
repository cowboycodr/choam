import os

from choam.choam import Choam
from choam.config_manager import ConfigManager
from choam.folder_structure import FolderStructure as FS

class Command:
    '''
    Generic command class for Choam's command-line-interface
    '''
    def __init__(
        self,
        ctx: Choam,
    ):
        self.ctx = ctx
        self.config = ConfigManager()

    def run(self):
        '''
        Command code that will be executed goes here
        '''

        pass

    @property
    def directory(self):
        return os.getcwd()

    @property
    def project_name(self):
        return FS.get_project_name()