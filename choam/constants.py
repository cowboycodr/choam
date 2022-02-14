import os
import sys
import platform
from pathlib import Path

# system details
OPERATING_SYSTEM = platform.system().lower()
PYTHON_INTERPRETER: str = sys.executable

# configurations
FOLDER_SEPERATOR: str
SETUP_FILE_NAME: str

# Processing platform specific configurations
if OPERATING_SYSTEM == "windows":
    FOLDER_SEPERATOR = "\\"
    SETUP_FILE_NAME = "setup"
    
    PYTHON_INTERPRETER = os.popen("where python").read().split('\n')[0]
    
else:
    FOLDER_SEPERATOR = "/"
    SETUP_FILE_NAME = "setup.py"
    
    PYTHON_INTERPRETER = os.popen("which python3").read().split("\n")[0]