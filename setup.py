from setuptools import setup, find_packages

setup(
    name="Choam",
    version="0.0.7",
    description="Python project scaffolder/manager",
    packages=find_packages(),
    keywords=['package', 'manager'],
    install_requires=['typing', 'fire', 'twine', 'findimports', 'toml', 'pkg_resources', 'wheel', 'pathlib', 'choam'],
    project_urls={
        'Source': 'https://github.com/cowboycodr/choam'
    },
)