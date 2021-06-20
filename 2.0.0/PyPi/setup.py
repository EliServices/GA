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
    name="ground_assistant",
    version="2.0.0",
    description="Library containing functions for the ga daemon.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://eliservices.servehttp.com/docs/ga_lib.html",
    author="EliServices",
    author_email="eliservices.server@gmail.com",
    license="Free for non-commercial use",
    classifiers=[
      "Intended Audience :: Developers",
      "Development Status :: 4 - Beta",
      "Environment :: Console",
      "License :: Free for non-commercial use",
      "Programming Language :: Python :: 3.8",
      "Operating System :: POSIX :: Linux",
      "Topic :: Database :: Database Engines/Servers"
    ],
    packages=["ground_assistant"],
    include_package_data=True,
    install_requires=["requests","mysql.connector","ogn-client","processnamer"]
)
