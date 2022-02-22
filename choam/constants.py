'''
Choam's constant variables

Mostly used for dynamic script configurations
in Choam.toml
'''

import sys
import platform

# system details
OPERATING_SYSTEM = platform.system().lower()
PYTHON_INTERPRETER: str = sys.executable

# configurations
FOLDER_SEPERATOR: str = "\\" if platform.system().lower() == "windows" else "/"
SETUP_FILE_NAME: str = "setup.py"
