![Static Badge](https://img.shields.io/badge/GUI%20status%3A-not_working-red?style=flat)
![Static Badge](https://img.shields.io/badge/CLI%20status%3A-working-darkgreen?style=flat)
![Static Badge](https://img.shields.io/badge/library%20status%3A-working-darkgreen?style=flat)


# FsaToolbox
A library to compute common operations on fsa automata.

### How to use
There are three ways to use this tool:
- Using the library in a python script
- Using a simple CLI interface
- Using a GUI interface *(currently not working)*

To use the python library
1) Build the lib from the root directory with:

```bash
python setup.py bdist_wheel
```
2) The wheel package is needed, you can install it with:
```bash
pip install wheel
```
3) After, locate the ".whl" file (usually in /dist) and install the lib with:
```bash
pip install "fullPathTo_whl"
```

To use the simple CLI interface:
1) Download the lastest build from the "Release" page
2) Unzip the downloaded folder
3) run "simpleCLI.exe"
Note that this doesn't require to have python installed.