from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in marketplace/__init__.py
from marketplace import __version__ as version

setup(
	name="marketplace",
	version=version,
	description="For Import Data",
	author="Marketplace",
	author_email="a@a.a",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
