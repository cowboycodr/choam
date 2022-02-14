from setuptools import setup, find_packages

setup(
    name="Choam",
    version="0.1.9",
    description="Python project scaffolder/manager",
    packages=find_packages(),
    keywords=['package', 'manager'],
    install_requires=['toml', 'fire', 'choam', 'typing', 'importlib', 'findimports', 'twine', 'wheel'],
    project_urls={
        'Source': 'https://github.com/cowboycodr/choam'
    },
)