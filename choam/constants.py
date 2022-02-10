import platform

FOLDER_SEPERATOR: str
SETUP_FILE_NAME: str

### Processing platform specfic constants

if platform.system().lower() == "windows":
    FOLDER_SEPERATOR = "\\"
    SETUP_FILE_NAME = "setup"
else:
    FOLDER_SEPERATOR = "/"
    SETUP_FILE_NAME = "setup.py"
