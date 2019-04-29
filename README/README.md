Inventory Script for the SUSE virtualization lab
================================================

_Inventory script written for the Virtualization Lab. On each computer run, returns predetermined system values and sends them to a centralized spreadsheet as to keep track of the status and stats of the machine. Project maintained at:_

[https://github.com/ckglxe95/Inventory](https://github.com/ckglxe95/Inventory)

Notes
-------------
- Must run with Python2.x
- Include commandline parameters
- Can (and probably should) be used with `salt-ssh`
- Designed for RPM to be built at [Open Build Service](http://build.opensuse.org)

TODO
-------------
- Upgrade the script from Python2.7 to Python3.x
- Refactor code to move from transliteration of system commands to actual emulated behavior
- (For GUI/TUI) Add machine and rack objects to more easily organize lab info
- Consider making needed fields modular, thus allowing more future fields to be added

Files
-------------
```bash
.
├── Inventory-1.0.tar.gz
|   └── Inventory-1.0
|       └── Inventory.py
├── Inventory.changes
├── Inventory.spec
├── Misc
│   └── Org_Inventory.sh
├── README
│   ├── README.md
│   └── Sample.png
└── xlutils-2.0.0.tar.gz

```

|   Authored by:   |   Last Date Modified:   |
|   ------------   |   -------------------   |
|   Christopher Kitras     |   2019-04-29  |

Instructions
-------------

Manual Building
------------------

**Compilation of script**  
_[PyInstaller](https://pypi.org/project/PyInstaller/) is the method most recommended_
1. `cd` to the directory where the script exists (i.e. `<downloaded/path/>invent_py`)
2. Ensure that `pyinstaller` is installed on the system (not the virtual environment of the said python project)
3. If not installed run `sudo pip install pyinstaller`
4. While in the directory of the script, run `pyinstaller --onefile Inventory.py`

**Execution of the script**
The script is still under active development. Ensure that the current user has sudo priviledges or is logged in as root. For now, the way it is run is via the commandline in the following format:


```bash
python2 /<path_to_script>/Inventory.py [TARGET FILE DIRECTORY]
```

**Execution of the binary**  
Fairly soon, a stand-alone binary file or zipped package will be made available for easier execution regardless of what python interpreter is being used. A link to this .zip will be made available [here](https://github.com/ckglxe95/Inventory/tree/master/invent_py/bin). If you decide to compile the code using `pyinstaller`, note the following:
    - Once the compilation of the script is complete, you will notice several folders that have been created. The only one you need to worry about is `dist`
    - Once inside `dist` you will see the executable name `Inventory`
To execute said binary, make sure you are a sudo user or logged in as root, and then enter in the following:
```bash
chmod +x Inventory
./Inventory [TARGET FILE DIRECTORY]
```

Packaging into RPM
------------------

The recommended platform to use to build an RPM is using SUSE's [Open Build Service](http://build.opensuse.org) which will allow for easier packaging and version tracking of this package. The project for `Inventory` currently exists [here](https://build.opensuse.org/package/show/home:christopolise/inventory). Using this package instead of a built binary will allow for platform flexibility (still within SUSE family at this point) and easier implementation within a salt state.

An RPM package is now available [here](https://download.opensuse.org/repositories/home:/christopolise) and can be downloaded via zypper:

```bash
# zypper ar -r http://download.opensuse.org/repositories/home:/christopolise/<distro's name>/home:christopolise.repo LabSysTools
# zypper in Inventory
```
After it has been sucessfully installed, the package can be run with
```bash
# Inventory [TARGE FILE DIRECTORY]
```

The Result
-------------
The purpose of the script is to write to a centralized XLS spreadsheet that will contain the information of all registered servers in the lab. The method of mass execution of the script on all servers is still being decided upon, but possible candidates for completing the job are either SALT or Ansible. 

![Sample Inventory Sheet](https://github.com/ckglxe95/Inventory/blob/master/README/Sample.png "Sample Inventory Sheet")

**Minutiae**  
1. The fields `Asset Tag, Platform/Pcode MM#, Software Development Products, VTd/IOMMU, SR_IOV, PCI, PCI-E, PCI-X, STABLE, Serial Remote Access, Power Remote Access, and Support by Intel Still` are not determined by the script as they are determined by out-of-box factors.
2. Red hostname means the machine is in critical condition
3. Yellow hostname means the machine is limited in capacity (i.e. no virtualization abilities)
4. Blue hostname means that one or more of the basic fields could not be determined and require more investigation
5. Green hostname means that the machine is in good condition.
6. The file belongs to root and cannot be edited unless the user is logged in under root
7. The file preserves user changes, therefore any corrections, investigative changes, and/or notes added to the file will be preserved after saving. Writing to the file via script after user editing will **not** affect the styling of the file.
8. The way it is written now, script does **not** detect duplicates, so if the script is run on the same machine twice, there **will** exist duplicates in the spreadsheet. It is suggested that if a new inventory of the lab be taken, _back up the old version of the file just in case_.


Implementation
-------------
_Given that this script is pretty robust, there are a number of ways that it could be run. More ways are likely to come over time as the script is updated and new neccesities arise._

**Single-host Execution**
The script binary, which can be made using the process described above, can be run as a stand-alone file, instructions for which can also be found above under the heading "Execution of binary", disregarding all directory-specific steps.

**Lab Execution (Multi-host)**
The best way to implement this script in a lab environment appears to be through the use of `salt-ssh`. The use of `salt-ssh` eliminates the need to install a salt minion on every machine that will be running the script. Rather, it refers to a roster file that provides a thorough list of all the hosts inspected including their login credentials. The following instructions below are based of the tutorials accredited below.

Prerequisites:
- A host machine on which you are willing to install SALT, host an NFS daemon, and set up a shared folder that will be accessed by all other machines in the lab.
- All machines that will be inspected by the script must have NFS and SSH allowed in the firewall. (Instructions will be included below)

[`salt-ssh` Installation (follow as needed)](https://www.sunayu.com/how-to-use-saltstack-salt-ssh/). A sample state file is provided below to outline how the client mounts and runs the command:

```sls
mount to master machine:
  mount.mounted:
    - name: /dir/where/nfs_mount/will/be/mounted
    - device: ip_of_master:/shared_folder
    - fstype: nfs
    
running the script:
  cmd.run:
    - name: /path_of_script/ /path_of_spreadsheet
```

Hosting an NFS (if you didn't already know)
(ON HOST)
1. Install the nfs package for the server
```bash
# zypper in nfs-kernel-server
```
2. Enable and start the proper services
```bash
# systemctl enable rpcbind
# systemctl start rpcbind
# systemctl start nfsserver
# chkconfig nfsserver on
```
3. Create and set permissions for shared directory
```bash
# mkdir /shared_dir/
# chmod 777 /shared_dir/
```
4. Make sure you allow clients to access the server
```bash
# vim /etc/exports
```
```vim
client_ip(rw,no_root_squash,no_all_squash,no_subtree_check)
```
5. Export the changes
```bash
# exportfs -a
```
6. Restart proper services to apply changes
```bash
# systemctl restart rpcbind
# systemctl restart nfsserver
```
7. (On SLES 15 or any SUSE distro that uses `firewall-cmd`, it is pretty easy to follow through with `yast`), allowing services through firewall
```bash
# firewall-cmd --permanent --add-service=nfs
# firewall-cmd --permanent --add-service=mountd
# firewall-cmd --permanent --add-service=rpc-bind
# firewall-cmd --reload
```

(ON_CLIENT)
1. Install nfs package for client
```bash
# zypper in nfs-utils
```
2. Allow SSH and NFS through firewall
```bash
# firewall-cmd --permanent --add-service=ssh
# firewall-cmd --permanent --add-service=nfs
# firewall-cmd --reload
# systemctl enable sshd
```

There is more testing to be done, but basically one can run the `salt-ssh` as explained in the tutorial linked above using a state file that will mount the shared drive to the client in question and have the client run the script, writing to the same spreadsheet, therefore updating the lab serially in one blow.

**Portable Execution**
The executable (although still SUSE specific) can be taken to any machine via USB, NFS mount, etc. and executed thusly:
```bash
# ./Inventory .
```
This will write the spreadsheet to the current directory, which in turn can be carried to different machines, editing the same spreadsheet.

Known issues
-------------
- Refactoring needed:
    - lscpu
    - /proc/cpuinfo
- Listing all of the harddrives and making info more reliable needed
