import os
import toml

class ConfigManager:
  def __init__(self) -> None:
    self.__directory = os.getcwd()
    self.__filepath = f"{self.__directory}\\Choam.toml"
    
    with open(self.__filepath, "r") as f:
      self.__configurations = toml.loads(
        f.read()
      )

  @property
  def configurations(self):
    return self.__configurations