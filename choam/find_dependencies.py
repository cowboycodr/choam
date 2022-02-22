'''
find_dependencies finds project dependencies
and adds them to Choam.tomls
'''

import importlib
import os
import sys
from pathlib import Path

import findimports
import toml


def _find_dependencies(project_path: Path, project_name):
    """
    Find all dependencies of a given project

    :project_path: path to project

    :project_name: name of the project // necesarry for
    `Choam` to know the exact location of the project
    all of the project files.
    """

    ignore_deps = [
        "os",
        "sys",
        "subprocess",
        "pkg_resources",
        "choam",
        "importlib",
        "pathlib",
    ]

    import_info = set()

    files = Path(Path(project_path / project_name).absolute()).rglob("*.py")

    for file_name in files:
        import_info.update(findimports.find_imports(str(file_name)))

    dependencies = set()

    for imp in import_info:
        # Simplfying output to just module name
        depedency = repr(imp).split("'")[1]

        if depedency.startswith(project_name):
            continue

        if depedency in sys.builtin_module_names:
            continue

        if depedency in ignore_deps:
            continue

        dependencies.add(repr(imp).split("'")[1].split(".")[0])

    return dependencies


def find_dependencies():
    """
    Syntactic sugar for `_find_dependencies()`

    Automatically specifies the arguments
    `_find_dependencies()` for `Choam`'s needs.
    """

    project_path = Path(os.getcwd()).absolute()
    with open(f"{os.getcwd()}/Choam.toml", "r", encoding="utf-8") as file:
        config = toml.loads(file.read())

        project_name = config["package"]["name"]
        ignored_deps = config["modules-ignore"]

    found_depedencies = _find_dependencies(project_path, project_name)
    dependencies = []

    for dep in found_depedencies:
        if not importlib.util.find_spec(dep):
            continue

        if dep in ignored_deps:
            continue

        dependencies.append(dep)

    return dependencies


if __name__ == "__main__":
    print(find_dependencies())
