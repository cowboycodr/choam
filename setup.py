import pathlib
from setuptools import setup, find_packages

directory = pathlib.Path(__file__).parent
long_description = (directory / "README.md").read_text()

setup(
    name="Choam",
	version="1.0.1",
    description="Python project scaffolder/manager",
    packages=["choam"],
    keywords=['package', 'manager'],
	install_requires=['fire', 'toml', 'twine', 'wheel', 'choam', 'typing', 'autoapi', 'findimports'],
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
