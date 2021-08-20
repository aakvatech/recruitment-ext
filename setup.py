from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in recruitment_ext/__init__.py
from recruitment_ext import __version__ as version

setup(
	name="recruitment_ext",
	version=version,
	description="Recruitment Extenstion for ERPNext",
	author="Aakvatech Limited",
	author_email="info@aakvatech.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
