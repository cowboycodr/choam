def create_setup_file(
  name: str, 
  version: str, 
  description: str, 
  keywords: "list[str]", 
  modules: "dict[str]",
  repo_url: str
  ):
  '''
  Generate basic setup.py file contents
  
  Package lists are currently generated automatically
  
  Arguments:
    @name - project name
    @version - current version
  '''
  
  return '\n'.join([
    'from setuptools import setup, find_packages',
    '',
    'setup(',
    f'    name="{name}",',
    f'    version="{version}",',
    f'    description="{description}",',
    f'    packages=find_packages(),',
    f'    keywords={keywords},',
    f'    install_requires={[key for key in modules.keys()]},',
    '    project_urls={',
    f"        'Source': '{repo_url}'",
    "    },",
    ')'
  ])