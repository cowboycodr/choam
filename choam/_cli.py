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
    '''
    Deliver named arguments to CLI object methods
    
    Specifying a cli-command method (example):
    ```
    class SomeObject():
      def __init__(self, ...arguments):
        pass
        
      # non-command method definitions start with an underscore
      def _command(arguments: list):
        # do something
        
      # cli-command method defintion example
      def command(name: str, age: int, extras: list):
        # MAKE SURE to specify a type after the colon 
      
        # do something
    ```
    '''
    
    methods = self._get_methods(self.__object)
    
    if command not in methods:
      print(f"'{command}' is not assosciated with '{self.__object.__name__}'")
      return
    
    method = getattr(
      self.__object,
      command
    )
    
    if len(sys.argv) > 2:
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
      
      method(**args_dict)
    else:
      method()