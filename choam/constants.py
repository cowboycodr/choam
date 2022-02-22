import os
import sys
import platform
from pathlib import Path

# system details
OPERATING_SYSTEM = platform.system().lower()
PYTHON_INTERPRETER: str = sys.executable

# configurations
FOLDER_SEPERATOR: str = "\\" if platform.system().lower() == "windows" else "/"
SETUP_FILE_NAME: str = "setup.py"
