Inventory Script for the SUSE virtualization lab
================================================

_Inventory script written for the Virtualization Lab. On each computer run, returns predetermined system values and sends them to a centralized spreadsheet as to keep track of the status and stats of the machine. Project maintained at:_

[https://github.com/ckglxe95/Inventory](https://github.com/ckglxe95/Inventory)

Notes
-------------
- Must run with Python2.x
- Compiled binary soon to be included

Files
-------------
```bash
.
├── invent_py
│   ├── Inventory.py
│   ├── Inventory-test.ods
│   └── requirements.txt
├── Org_Inventory.sh
└── README.md  
```

|   Authored by:   |   Last Date Modified:   |
|   ------------   |   -------------------   |
|   Christopher Kitras     |   2018-08-03  |

Instructions
-------------
**Compilation of script**  
_[Pyinstaller](https://pypi.org/project/PyInstaller/) is the method most recommended_
1. `cd` to the directory where the script exists (i.e. `<downloaded/path/>invent_py`)
2. Ensure that `pyinstaller` is installed on the system (not the virtual environment of the said python project)
3. If not installed run `sudo pip install pyinstaller`
4. While in the directory of the script, run `pyinstaller Inventory.py`

**Execution of the script**
The script is still under active development. Ensure that the current user has sudo priviledges or is logged in as root. For now, the way it is run is via the commandline in the following format:


```bash
# python2 Inventory.py [TARGET FILE DIRECTORY]
```

**Execution of the binary**  
Fairly soon, a stand-alone binary file or zipped package will be made available for easier execution regardless of what python interpreter is being used. A link to this .zip will be made available [here](#). If you decide to compile the code using `pyinstaller`, note the following:
    - Once the compilation of the script is complete, you will notice several folders that have been created. The only one you need to worry about is `dist`
    - Once inside `dist`, `cd` into `Inventory` and inside you will find various libraries and folders, among which is the binary file `Inventory`
To execute said binary, make sure you are a sudo user or logged in as root, and then enter in the following:
```bash
# chmod +x Inventory
# ./Inventory [TARGET FILE DIRECTORY]
```

The Result
-------------
The purpose of the script is to write to a centralized ODS spreadsheet that will contain the information of all registered servers in the lab. The method of mass execution of the script on all servers is still being decided upon, but possible candidates for completing the job are either SALT or Ansible. 
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")



Known issues
-------------
- Refactoring needed:
    - lscpu
    - /proc/cpuinfo
- prerequisites() needs to check package list only once and search for the values
- Listing all of the harddrives and making info more reliable needed
