from setuptools import setup, find_packages

setup(
    name="Choam",
    version="0.1.2",
    description="Python project scaffolder/manager",
    packages=find_packages(),
    keywords=['package', 'manager'],
    install_requires=['findimports', 'typing', 'fire', 'toml', 'choam', 'pathlib'],
    project_urls={
        'Source': 'https://github.com/cowboycodr/choam'
    },
)