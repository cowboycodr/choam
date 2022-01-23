from .folder_structure import FolderStructure as FS
from ._cli import CommandLineInterface as CLI

import os

class Choam:
  def __init__(self) -> None:
    pass
  
  def init(name: str):
    directory = os.getcwd()
    
    if FS.is_choam_project(directory):
      print("\n\tAlready a Choam project.")
      return
    
    with open("assets/.gitignore.txt") as f:
      gitignore = f.read()
    
    template = {
      f"\\{name}\\__main__.py": "",
      f"\\{name}\\__init__.py": "__version__ == '0.1'",
      f"Choam.toml": f'[package]\nname = "{name}\nversion = "0.0.1"\ndescription = ""',
      f"README.md": f"# {name}\n#### This project was constructed with [Choam](https://github.com/cowboycodr/choam)",
      f".gitignore": gitignore
    }
    
    FS.construct_from_dict(template, directory)
  
  def new(name: str):
    directory = os.getcwd()
    
    with open(os.path.abspath("choam\\assets\.gitignore.txt"), "r") as f:
      gitignore = f.read()
    
    # Choam project template
    template = {
      f"\\{name}\\{name}\\__main__.py": "",
      f"\\{name}\\{name}\\__init__.py": "__version__ == '0.1'",
      f"\\{name}\\Choam.toml": f'[package]\nname = "{name}\nversion = "0.0.1"\ndescription = ""',
      f"\\{name}\\README.md": f"# {name}\n#### This project was constructed with [Choam](https://github.com/cowboycodr/choam)",
      f"\\{name}\\.gitignore": gitignore
    }
    
    FS.construct_from_dict(template, directory)
    
if __name__ == '__main__':
  CLI(Choam)