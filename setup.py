from setuptools import setup, find_packages

setup(
    name="Choam",
    version="0.1.1",
    description="Python project scaffolder/manager",
    packages=find_packages(),
    keywords=['package', 'manager'],
    install_requires=['choam', 'typing', 'wheel', 'findimports', 'toml', 'twine', 'fire', 'pathlib'],
    project_urls={
        'Source': 'https://github.com/cowboycodr/choam'
    },
)