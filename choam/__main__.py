import os
import sys
import shutil
import pkg_resources
from typing import Optional

from choam.create_setup_file import create_setup_file
from choam.find_dependencies import find_dependencies
from choam.folder_structure import FolderStructure as FS
from choam.gitignore import gitignore

import toml
import fire
import subprocess

class Choam:
  def __init__(self):
    pass

  def _get_config():
    with open(f"{os.getcwd()}/Choam.toml", "r") as f:
      return toml.loads(
        f.read()
      )
    
  def _set_config(content: str):
    with open(f"{os.getcwd()}/Choam.toml", "w") as f:
      f.write(str(content))
  
  def _log(message: str):
    print(f"\n\t{message}")
    print()
    
  def _log_multiple(messages: "list[str]"):
    print()
    for message in messages:
      print(f'\t{message}')
    print()
  
  def _adapt(self, directory: str, name: str):
    '''
    Adapt an existing project directory to Choam's structure
    '''

    for f in os.listdir(directory):
      dest = os.path.join(directory, name, f)

      try:
        os.makedirs('/'.join(dest.split("/")[:-1]))
      except FileExistsError:
        pass
      
      try:
        shutil.move(f, dest)
      except:
        pass

    template = {
      f"\\Choam.toml": f'[package]\nname="{name}\nversion="0.0.0"\ndescription=""\nrepo="*required*"\nkeywords=[]\n\n[modules-ignore]\n\n[modules]',
      f"\\README.md" : f"{name}\n###This project was structure with [Choam](https://github.com/cowboycodr/choam)",
      f"\\.gitignore": gitignore
    }

    FS.construct_from_dict(template, directory)

  def init(self, adapt: Optional[bool] = None):
    '''
    Initalize a new Choam project in the working 
    directory
    '''

    directory = os.getcwd()
    name = directory.split("/")[-1]
    
    if FS.is_choam_project(directory):
      Choam._log("Already a Choam project.")
      return
    
    if adapt:
      self._adapt(directory, name)

      return

    template = {
      f"{directory}\\{name}\\__main__.py": "",
      f"{directory}\\{name}\\__init__.py": "__version__ == '0.1'",
      f"{directory}\\Choam.toml": f'[package]\nname = "{name}\nversion = "0.0.1"\ndescription = ""\n\n[modules-ignore]\n\n[modules]',
      f"{directory}\\README.md": f"# {name}\n#### This project was constructed with [Choam](https://github.com/cowboycodr/choam)",
      f"{directory}\\.gitignore": gitignore
    }
    
    FS.construct_from_dict(template, directory)
  
  def cleanup(self):
    '''
    Remove build directories discharged from `$ choam publish` 
    '''

    project_name = Choam._get_config()['package']['name']

    build_directories = [
      "build",
      f"{project_name}.egg-info",
      "dist"
    ]

    if project_name in build_directories:
      Choam._log_multiple(
        [
          "Cannot cleanup project that matches names with build directories list",
        f"{project_name} is a reserved directory name."
        ]
      )
      return

    for dirname in build_directories:
      path = f"{os.getcwd()}/{dirname}"

      if not os.path.exists(path):
        continue

      shutil.rmtree(path)


  def new(self, name: str):
    '''
    Create a new directory and initalize a Choam project
    inside of it
    '''

    directory = os.getcwd()
      
    folder_name = name.lower()
    
    # Choam project template
    template = {
      f"\\{folder_name}\\{folder_name}\\__main__.py": "",
      f"\\{folder_name}\\{folder_name}\\__init__.py": "__version__ == '0.1'",
      f"\\{folder_name}\\Choam.toml": f'[package]\nname = "{name}"\nversion = "0.0.1"\ndescription = ""\n\n[modules]\nchoam = "*"',
      f"\\{folder_name}\\README.md": f"# {name}\n#### This project was constructed with [Choam](https://github.com/cowboycodr/choam)",
      f"\\{folder_name}\\.gitignore": gitignore
    }
    
    FS.construct_from_dict(template, directory)
    
  def run(self, relative_path: Optional[str] = None):
    '''
    Run `Choam`'s default entry point or specify
    a relative filepath for Choam to run.

    :relative_path: specific file for `Choam` to run
    '''
    
    if not FS.is_choam_project():
      Choam._log("Not a Choam project.")
      return
    
    project_folder = Choam._get_config()['package']['name'].lower()
    
    if not relative_path:
      subprocess.call(
        [sys.executable, "-m", project_folder]
      )
      return

    subprocess.call(
      [sys.executable, os.path.join(os.getcwd(), project_folder, relative_path)]
    )
    
  def setup(self):
    '''
    Setup configurations for PyPi in `setup.py`.

    Additional configurations may be done to `setup.py`
    after this command has been run.
    '''

    directory = os.getcwd()
    
    config = Choam._get_config()
  
    package_config = config['package']
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
      
    modules = config['modules']
    
    template = {
      f"\\setup.py": create_setup_file(
        name,
        version,
        description,
        keywords,
        modules,
        repo_url
      )
    }

    self.find_dependencies()
    
    FS.construct_from_dict(template, f"{directory}\\")
    
    Choam._log_multiple(
      [
        f"Successfully setup '{name}' for PyPi publication",
        f"Use '$ choam publish' when configurations have been set"
      ]
    )
    
  def add(self, dependency_name: str, install: Optional[bool] = None, ignore: Optional[bool] = None):
    '''
    Add a required depedency to the depdency list
    '''

    config = Choam._get_config()

    if ignore:
      config['modules-ignore'][dependency_name] = "*"
      config['modules'].pop(dependency_name)

      Choam._set_config(toml.dumps(config))

      return

    config['modules'][dependency_name] = "*"

    Choam._set_config(toml.dumps(config))
    
    if install: self.install(find_dependencies=False)

  def install(self, find_dependencies: Optional[bool] = None):
    config = Choam._get_config()

    if find_dependencies:
      self.find_dependencies()

    required_mods = {mod for mod in config['modules']}
    installed_mods = {mod.key for mod in pkg_resources.working_set}
    missing_mods = required_mods - installed_mods

    # Key: Module name, Value: Module version
    mod_ver = config['modules']

    for mod in missing_mods:
      Choam._log(f"Installing {mod}")

      module_string = f"{mod}=={mod_ver[mod]}" if mod_ver[mod] != "*" else f"{mod}--upgrade"
      upgrade_module = module_string.endswith('--upgrade')

      subprocess.call([sys.executable, "-m", "pip", "install", module_string.replace("--upgrade", ""), "--upgrade" if upgrade_module else ""])
    
  def publish(self):
    self.add("twine")
    self.add("wheel")
    self.install()

    Choam._log("Attempting real publication to https://test.pypi.org/legacy")
    
    subprocess.call([sys.executable, "-m", "setup.py", "sdist", "bdist_wheel"])
    subprocess.call([sys.executable, "-m", "twine", "upload", "dist/*"])

    Choam._log("Real publication attempt completed")

  def find_dependencies(self):
    '''
    Automatically search project files for imported
    depedencies and add them to `Choam.toml` as well
    as setup
    '''

    depedencies = find_dependencies()
    new_config = Choam._get_config()
    new_config['modules'] = {dep: "*" for dep in sorted(list(depedencies), key=len)}

    Choam._set_config(toml.dumps(new_config))
  
if __name__ == '__main__':
  fire.Fire(Choam())