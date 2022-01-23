def create_setup_file(name: str, version: str, description: str):
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
    f'    packages=["{name.lower()}"],',
    f'    version="{version}",',
    f'    description="{description}",',
    f'    packages=find_packages()',
    ')'
  ])