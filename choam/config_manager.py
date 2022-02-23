import os

import toml
from pathlib import Path

from choam.constants import FOLDER_SEPERATOR

class ConfigManager:
    def __init__(self):
        self.DIRECTORY = os.getcwd()
        self.CHOAM_CONFIG_PATH = f"{self.DIRECTORY}{FOLDER_SEPERATOR}Choam.toml"

    def get(self) -> "dict[str, any]":
        '''
        Capture current configurations state in `TOML` form
        '''

        return toml.loads(Path(self.CHOAM_CONFIG_PATH) \
                .read_text(encoding='utf-8'))

    def set(self, _new: str) -> None:
        '''
        Write new configurations in str or toml form
        '''

        Path(self.CHOAM_CONFIG_PATH) \
                .write_text(toml.dumps(_new), encoding="utf-8")

    def is_section(self, section_name: str) -> bool:
        return section_name in self.get().keys()