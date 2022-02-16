from importlib_metadata import entry_points
from setuptools import setup, find_packages
import pathlib

directory = pathlib.Path(__file__).parent
long_description = (directory / "README.md").read_text()

setup(
    name="Choam",
	version="0.1.15",
    description="Python project scaffolder/manager",
    packages=["choam"],
    keywords=['package', 'manager'],
	install_requires=['fire', 'toml', 'choam', 'twine', 'wheel', 'typing', 'importlib', 'findimports'],
    project_urls={
        'Source': 'https://github.com/cowboycodr/choam'
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "choam = choam:main"
        ]
    }
)