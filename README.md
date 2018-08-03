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

AUTHORED BY: Chris Kitras
LAST DATE MODIFIED: 2018-08-02

|   Authored by:   |   Last Date Modified:   |
|   ------------   |   -------------------   |
|   Christopher Kitras     |   2018-08-03  |

Known issues
-------------
- Refactoring needed:
    - lscpu
    - /proc/cpuinfo
- prerequisites() needs to check package list only once and search for the values
- Listing all of the harddrives and making info more reliable needed
