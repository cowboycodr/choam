from setuptools import setup, find_packages

setup(
    name="Choam",
    version="0.0.7",
    description="Python project scaffolder/manager",
    packages=find_packages(),
    keywords=['package', 'manager'],
    install_requires=['toml', 'findimports', 'fire', 'subprocess', 'os', 'pathlib', 'sys', 'typing', 'choam'],
    project_urls={
        'Source': 'https://github.com/cowboycodr/choam'
    },
)