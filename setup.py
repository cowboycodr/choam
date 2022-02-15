from setuptools import setup, find_packages

setup(
    name="Choam",
    version="0.1.10",
    description="Python project scaffolder/manager",
    packages=find_packages(),
    keywords=['package', 'manager'],
    install_requires=['choam', 'importlib', 'toml', 'findimports', 'typing', 'fire'],
    project_urls={
        'Source': 'https://github.com/cowboycodr/choam'
    },
)