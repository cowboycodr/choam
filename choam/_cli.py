# class Application(cli("<cli_name>")):
#   def create(self):
#     #  do something

import sys
from inspect import signature

class CommandLineInterface:
  '''
  Command line interface class for managing 
  methods to commands
  '''
  
  @staticmethod
  def _check_arguments():
    return len(sys.argv) > 1
  
  @staticmethod
  def _get_methods(_object):
    return [
      method for method in dir(_object) if method.startswith('_') is False
    ]
  
  def __init__(self, _object) -> None:
    self.__object = _object
    self.__arguments = sys.argv
    
    if not self._check_arguments():
      return
    
    self.command(self.__arguments[1])
    
  def command(self, command: str):
    methods = self._get_methods(self.__object)
    
    if command.lower() not in methods:
      return
    
    method = getattr(
      self.__object,
      command
    )
    
    arg_signature = str(signature(method)).replace('(', '').replace(')', '')
    
    args_list = []
    
    for arg in arg_signature.split(","):
      arg = arg.split(":")[0].strip()
      
      args_list.append(arg)
    
    args_dict = {}
    for arg_index, arg in enumerate(args_list):
      
      if arg_index < len(args_list) - 1:
        arg_value = sys.argv[arg_index + 2]
        
      elif len(sys.argv) - 1 > arg_index + 1:
        arg_value = sys.argv[arg_index + 2:]
        
        if len(arg_value) == 1: 
          arg_value = arg_value[0]
        
      else:
        raise IndexError(f"Failed to run command: '{command}': was not supplied enough arguments")
      
      args_dict[arg] = arg_value
    
    print(args_dict)
    
    # method(**args_dict)