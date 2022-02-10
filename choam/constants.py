import platform

FOLDER_SEPERATOR: str

### Processing platform specfic constants

if platform.system().lower() == "windows":
    FOLDER_SEPERATOR = "\\"
else:
    FOLDER_SEPERATOR = "/"
