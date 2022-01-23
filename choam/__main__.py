from .folder_structure import FolderStructure as FS
from ._cli import CommandLineInterface as CLI

import os

class Choam:
  def __init__(self) -> None:
    pass
  
  def new(name: str):
    # TODO: Programmatically create folder structure
    
    with open(os.path.abspath("choam\\assets\.gitignore.txt"), "r") as f:
      gitignore = f.read()
    
    template = {
      f"\\{name}\\{name}\\__main__.py": "",
      f"\\{name}\\{name}\\__init__.py": "__version__ == '0.1'",
      f"\\{name}\\assets"
      f"\\{name}\\Choam.toml": "{\n\n}",
      f"\\{name}\\README.md": f"# {name}",
      f"\\{name}\\.gitignore": gitignore
    }
    
    FS.construct_from_dict(template, os.getcwd())
    
if __name__ == '__main__':
  CLI(Choam)