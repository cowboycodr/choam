import os
from pathlib import Path

import toml
import findimports

def _find_dependencies(project_path: Path, project_name):
    import_info = set()

    files = Path(
        Path(project_path / project_name).absolute()
    ).glob("*.py")

    for f in files:
        import_info.update(
            findimports.find_imports(str(f))
        )

    dependencies = set()

    for imp in import_info:
        # Simplfying output to just module name
        depedency = repr(imp).split("'")[1]

        if depedency.startswith(project_name):
            continue

        dependencies.add(
            repr(imp).split("'")[1].split(".")[0]
        )

    return dependencies

def find_dependencies():
    project_path = Path(os.getcwd()).absolute()
    with open(f"{os.getcwd()}/Choam.toml", "r") as f:
        project_name = toml.loads(
            f.read()
        )['package']['name']

    return _find_dependencies(project_path, project_name)

if __name__ == '__main__':
    print(find_dependencies())