# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="GA",
    version="0.1.0",
    description="Library containing functions for working with the ogn-network.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://GA.readthedocs.io/",
    author="Elias Kremer",
    author_email="eliservices.server@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha"
        "Intended Audience :: Developers",
        "License :: Free for non-commercial use",
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX :: Linux"
    ],
    packages=["GA"],
    include_package_data=True,
    install_requires=["numpy"]
)