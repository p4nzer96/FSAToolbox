# FsaToolbox
A library to compute common operations on fsa automata.

### How to use
There are two ways to use this tool:
- Using the library in a python script
- Using a simple CLI interface

To use the python library
- build the lib from the root directory with:
```
python setup.py bdist_wheel
```
The wheel package is needed, you can install it with:
```
pip install wheel
```
After, locate the ".whl" file (usually in /dist) and install the lib with:
```
pip install "fullPathTo_whl"
```

To use the simple CLI interface:
- Download the lastest build from the "Release" page
- unzip the folder
- run "simpleCLI.exe"
Note that this doesn't require to have python installed.