from .folder_structure import FolderStructure as FS
from ._cli import CommandLineInterface as CLI
from .config_manager import ConfigManager

import os
class Choam:
  def __init__(self) -> None:
    pass
  
  def _log(message: str):
    print(f"\n\t{message}")
  
  def init(name: str):
    directory = os.getcwd()
    
    if FS.is_choam_project(directory):
      Choam._log("Already a Choam project.")
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
      
    folder_name = name.lower()
    
    # Choam project template
    template = {
      f"\\{folder_name}\\{folder_name}\\__main__.py": "",
      f"\\{folder_name}\\{folder_name}\\__init__.py": "__version__ == '0.1'",
      f"\\{folder_name}\\Choam.toml": f'[package]\nname = "{name}\nversion = "0.0.1"\ndescription = ""',
      f"\\{folder_name}\\README.md": f"# {name}\n#### This project was constructed with [Choam](https://github.com/cowboycodr/choam)",
      f"\\{folder_name}\\.gitignore": gitignore
    }
    
    FS.construct_from_dict(template, directory)
    
  def run():
    '''
    Run choam project main file
    '''
    
    if not FS.is_choam_project():
      Choam._log("Not a Choam project.")
      return
    
    folder_name = ConfigManager().configurations['package']['name'].lower()
    
    os.system(
      f"python -m {folder_name}"
    )
    
if __name__ == '__main__':
  CLI(Choam)