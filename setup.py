from setuptools import setup, find_packages

setup(
    name="Choam",
    packages=["choam"],
    version="0.0.1",
    description="Python project scaffolder/manager",
    packages=find_packages(),
    keywords=[],
    install_requires=['flask'],
    project_urls={
        'Source': ''
    },
)