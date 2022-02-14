import os
import sys
from pathlib import Path
import platform

# configurations
FOLDER_SEPERATOR: str
SETUP_FILE_NAME: str

### Processing platform specific configurations
if platform.system().lower() == "windows":
    FOLDER_SEPERATOR = "\\"
    SETUP_FILE_NAME = "setup"
else:
    FOLDER_SEPERATOR = "/"
    SETUP_FILE_NAME = "setup.py"
    
# system details
PYTHON_INTERPRETER = sys.executable