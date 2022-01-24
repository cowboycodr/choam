from setuptools import setup, find_packages

setup(
    name="Choam",
    version="0.0.3",
    description="Python project scaffolder/manager",
    packages=find_packages(),
    keywords=['package', 'manager'],
    install_requires=['toml', 'twine', 'fire'],
    project_urls={
        'Source': 'https://github.com/cowboycodr/choam'
    },
)