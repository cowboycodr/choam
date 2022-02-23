import os

import toml
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.DIRECTORY = os.getcwd()

    def get(self) -> "dict[str, any]":
        '''
        Capture current configurations state in `TOML` form
        '''

        return toml.loads(Path(self.DIRECTORY / "Choam.toml") \
                .read_text(encoding='utf-8'))

    def set(self, _new: str) -> None:
        '''
        Write new configurations in str or toml form
        '''

        Path(self.DIRECTORY / "Choam.toml") \
                .write_text(toml.dumps(_new), encoding="utf-8")