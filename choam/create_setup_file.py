import os
import pathlib

from choam.find_dependencies import find_dependencies

def create_setup_file(
    name: str,
    version: str,
    description: str,
    keywords: "list[str]",
    dependencies: "list",
    repo_url: str,
):
    """
    Generate basic setup.py file contents
    Package lists are currently generated automatically
    Arguments:
      @name - project name
      @version - current version
    """

    new_dependencies = set(find_dependencies())
    for dep in dependencies:
        new_dependencies.add(dep)

    dependencies = new_dependencies

    return "\n".join(
        [
            "from setuptools import setup, find_packages",
            "",
            "setup(",
            f'    name="{name}",',
            f'    version="{version}",',
            f'    description="{description}",',
            f"    packages=find_packages(),",
            f"    keywords={keywords},",
            f"    install_requires={[dep for dep in dependencies]},",
            "    project_urls={",
            f"        'Source': '{repo_url}'",
            "    },",
            ")",
        ]
    )