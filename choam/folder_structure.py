import os

class FolderStructure:
  '''
  `Choam's` folder structure consturction/destruction
  manager class
  '''
  
  @staticmethod
  def _create_file(filepath: str, content: "str | None") -> str:
    file_name = filepath.split("\\")[-1]
    folder_path = filepath.replace(file_name, '')
    
    if not os.path.exists(folder_path):
      os.makedirs(folder_path)
      
    with open(filepath, "w") as file:
      file.write(content if content else "")
      
    return filepath
  
  @staticmethod
  def construct_from_dict(_dict: dict, output_dir: str):
    '''
    Construct folder structure from dictionary
    '''
    
    output_dir = os.path.abspath(output_dir)
    
    for file_name in _dict.keys():
      FolderStructure._create_file(output_dir + file_name, _dict[file_name])