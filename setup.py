from setuptools import setup, find_packages

setup(
    name="Choam",
    version="0.1.3",
    description="Python project scaffolder/manager",
    packages=find_packages(),
    keywords=['package', 'manager'],
    install_requires=['twine', 'toml', 'wheel', 'shutil', 'choam', 'fire', 'findimports', 'pathlib', 'typing'],
    project_urls={
        'Source': 'https://github.com/cowboycodr/choam'
    },
)