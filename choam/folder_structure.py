import os


class FolderStructure:
    """
    `Choam's` folder structure consturction/destruction
    manager class
    """

    @staticmethod
    def is_choam_project(_dir: "str | None" = None) -> bool:
        """
        Returns true if the directory passed in
        is a Choam project
        """

        if not _dir:
            _dir = os.getcwd()

        if not os.path.exists(_dir):
            return

        return "Choam.toml" in os.listdir(os.path.abspath(_dir))

    def is_publishable(_dir: "str | None" = None):
        """'
        Returns True if the directory fits
        Choam's publication requirements
        """

        if not _dir:
            _dir = os.getcwd()

        if not os.path.exists(_dir):
            return

        return "setup.py" in os.listdir(os.path.abspath(_dir))

    @staticmethod
    def _create_file(filepath: str, content: "str | None") -> str:
        filepath = os.path.abspath(filepath)
        filepath = filepath.replace("\\", "/")

        file_name = filepath.split("/")[-1]
        folder_path = filepath.replace(file_name, "")

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(filepath, "w") as file:
            file.write(content if content else "")

        return filepath

    @staticmethod
    def construct_from_dict(_dict: dict, output_dir: str):
        """
        Construct folder structure from dictionary
        """

        output_dir = os.path.abspath(output_dir)

        for file_name in _dict.keys():
            FolderStructure._create_file(f"{output_dir}\\{file_name}", _dict[file_name])
