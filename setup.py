from setuptools import setup, find_packages
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="fsatoolbox",
    packages=find_packages(),
    version="0.01",
    description="A ToolBox to work with FSA automata",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dennis Loi & Andrea Panzino",
    install_requires=["numpy", "pandas", "tabulate"]
)
