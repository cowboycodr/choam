from setuptools import setup, find_packages

setup(
    name="Choam",
	version="0.1.11",
    description="Python project scaffolder/manager",
    packages=find_packages(),
    keywords=['package', 'manager'],
	install_requires=['fire', 'toml', 'choam', 'twine', 'wheel', 'typing', 'importlib', 'findimports', 'flask'],
    project_urls={
        'Source': 'https://github.com/cowboycodr/choam'
    },
)