from setuptools import setup, find_packages

setup(
    name="Choam",
    version="0.1.6",
    description="Python project scaffolder/manager",
    packages=find_packages(),
    keywords=['package', 'manager'],
    install_requires=['fire', 'importlib', 'pathlib', 'choam', 'findimports', 'toml', 'typing'],
    project_urls={
        'Source': 'https://github.com/cowboycodr/choam'
    },
)