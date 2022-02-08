from setuptools import setup, find_packages

setup(
    name="Choam",
    version="0.0.6",
    description="Python project scaffolder/manager",
    packages=find_packages(),
    keywords=['package', 'manager'],
    install_requires=['sys', 'fire', 'pathlib', 'toml', 'choam', 'findimports', 'subprocess', 'os'],
    project_urls={
        'Source': 'https://github.com/cowboycodr/choam'
    },
)