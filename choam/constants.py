import os
from pathlib import Path
import platform

# configurations
FOLDER_SEPERATOR: str
SETUP_FILE_NAME: str

# system details
PYTHON_INTERPRETER: str = (
    str(Path(os.__file__).parents[2]) + FOLDER_SEPERATOR + "python.exe"
)

### Processing platform specific configurations
if platform.system().lower() == "windows":
    FOLDER_SEPERATOR = "\\"
    SETUP_FILE_NAME = "setup"
else:
    FOLDER_SEPERATOR = "/"
    SETUP_FILE_NAME = "setup.py"
