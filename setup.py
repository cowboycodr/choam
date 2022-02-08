from setuptools import setup, find_packages

setup(
    name="Choam",
    version="0.1.5",
    description="Python project scaffolder/manager",
    packages=find_packages(),
    keywords=['package', 'manager'],
    install_requires=['toml', 'pathlib', 'choam', 'fire', 'shutil', 'findimports', 'importlib', 'typing'],
    project_urls={
        'Source': 'https://github.com/cowboycodr/choam'
    },
)