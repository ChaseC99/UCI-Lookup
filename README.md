# UCI-Lookup
Tool to look up multiple UCI students at a time.
Currently, you can only search for a student by email or UCInetID.  
NOTE: you must be on the UCI VPN for UCI-Lookup to work

Look up options include:  
    [1] Single Search - Look up one person  
    [2] Multi Search - Look up multiple people at a time  
    [3] Multi Search From File - Look up multiple people from a file with a search querey on each line

## Installation
| Step | Instruction | Command |
| --- | --- | --- |
| 1 | Clone the repository | `git clone`  |
| 2 | Navigate into the repo | `cd UCI-Lookup` |
| 3 | Setup a virtual environment | `python3 -m venv env` |
| 4 | Activate the virtual environment | `source env/bin/activate` |
| 5 | Download ldap3 | `pip3 install ldap3` |

## Usage
Start up the Python script with `python3 uci-lookup.py` and simply follow the command line prompts.

## Dependencies
- [`ldap3`](https://pypi.org/project/ldap3/)  

## UCI Privacy Policy
This tool may only be used in accordance with the [UCI Directory](https://directory.uci.edu/) Privacy Policy. 
> This directory has been compiled for the use and convenience of the faculty, staff, students, and affiliates of the University of California, Irvine and others dealing with UC Irvine. It is the property of the Regents of the University of California. In accordance with the California Information Practices Act, neither this directory nor the information contained herein may be used, rented, distributed, or sold for commercial purposes. Compilation or redistribution of information from this directory is strictly forbidden.
