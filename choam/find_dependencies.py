import os
import sys
import importlib
from pathlib import Path

import toml
import findimports


def _find_dependencies(project_path: Path, project_name):
    """
    Find all dependencies of a given project

    :project_path: path to project

    :project_name: name of the project // necesarry for
    `Choam` to know the exact location of the project
    all of the project files.
    """

    ignore_deps = ["os", "sys", "subprocess", "pkg_resources"]

    import_info = set()

    files = Path(Path(project_path / project_name).absolute()).rglob("*.py")

    for f in files:
        import_info.update(findimports.find_imports(str(f)))

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
    with open(f"{os.getcwd()}/Choam.toml", "r") as f:
        config = toml.loads(f.read())

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
