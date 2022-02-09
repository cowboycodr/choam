from setuptools import setup, find_packages

setup(
    name="Choam",
    version="0.1.5",
    description="Python project scaffolder/manager",
    packages=find_packages(),
    keywords=['package', 'manager'],
    install_requires=['pathlib', 'toml', 'importlib', 'findimports', 'choam', 'typing', 'fire'],
    project_urls={
        'Source': 'https://github.com/cowboycodr/choam'
    },
)