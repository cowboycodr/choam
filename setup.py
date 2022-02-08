from setuptools import setup, find_packages

setup(
    name="Choam",
    version="0.1.0",
    description="Python project scaffolder/manager",
    packages=find_packages(),
    keywords=['package', 'manager'],
    install_requires=['wheel', 'twine', 'toml', 'pathlib', 'typing', 'findimports', 'choam', 'fire'],
    project_urls={
        'Source': 'https://github.com/cowboycodr/choam'
    },
)