import os

from choam._cli import CommandLineInterface as CLI
from choam.config_manager import ConfigManager
from choam.create_setup_file import create_setup_file
from choam.folder_structure import FolderStructure as FS

class Choam:
  def __init__(self) -> None:
    pass
  
  def _log(message: str):
    print(f"\n\t{message}")
    
  def _log_multiple(messages: list[str]):
    print()
    for message in messages:
      print(f'\t{message}')
  
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
    
  def setup():
    directory = os.getcwd()
    
    package_config = ConfigManager().configurations['package']
    
    name = package_config['name']
    version = package_config['version']
    
    try:
      description = package_config['description']
    except:
      description = ""
    
    try:
      repo_url = package_config['repo']
    except:
      repo_url = ''
    
    try:
      keywords = package_config['keywords']
    except:
      keywords = []
      
    modules = ConfigManager().configurations['modules']
    
    template = {
      f"setup.py": create_setup_file(
        name,
        version,
        description,
        keywords,
        modules,
        repo_url
      )
    }
    
    FS.construct_from_dict(template, f"{directory}\\")
    
    Choam._log_multiple(
      [
        f"Successfully setup '{name}' for PyPi publication",
        f"Use '$ choam publish' (not impl'd yet) when configurations have been set"
      ]
    )
    
if __name__ == '__main__':
  CLI(Choam)
