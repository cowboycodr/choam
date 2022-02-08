from setuptools import setup, find_packages

setup(
    name="Choam",
    version="0.1.4",
    description="Python project scaffolder/manager",
    packages=find_packages(),
    keywords=['package', 'manager'],
    install_requires=['fire', 'toml', 'choam', 'shutil', 'pathlib', 'findimports', 'typing'],
    project_urls={
        'Source': 'https://github.com/cowboycodr/choam'
    },
)