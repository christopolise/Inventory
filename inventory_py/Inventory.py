import subprocess
import os


def sudocheck():
    """
    Checks to see if user has sudo privileges
    :return: void
    """

    access = os.getuid()
    if access != 0:
        print('You must run this script as root or under sudo')
        exit(code=1)


def prereqcheck():
    """
    Checks for and installs prerequisites if necessary
    :return:
    """
    prerequisites = ['dmidecode', 'util-linux', 'ethtool', 'usbutils', 'gptfdisk', 'bc', 'emacs']
    for i in range(len(prerequisites)):
        rpm = subprocess.Popen(('rpm', '-qa', '--last'), stdout=subprocess.PIPE)
        try:
            output = subprocess.check_output(('grep', '-iw', prerequisites[i]), stdin=rpm.stdout)
        except Exception as e:
            output = None
        rpm.wait()
        if output is None:
            print('Installing dependency: ' + prerequisites[i])
            # subprocess.run(['zypper', '-n', 'install', prerequisites[i]])
            os.system('zypper -n install ' + prerequisites[i])
        else:
            print('Dependency ' + prerequisites[i] + ' is already satisfied')


def asset():
    return 'ASSET'


def hostname():
    pass


def pcode():
    return 'PCODE'


def mm():
    return 'MM'


def sdp():
    return 'SDP'


def serialnumber():
    pass


def makemodel():
    pass


def vendor():
    pass


def codename():
    pass


def cpuspeed():
    pass


def sockets():
    pass


def threads():
    pass


def hyperthreading():
    pass


def cpucores():
    pass


def ram():
    pass


def virttech():
    pass


def vtd():
    return 'VTD'


def hap():
    pass


def sriov():
    return 'SRIOV'


def numa():
    pass


def efi():
    pass


def pci():
    return 'PCI'


def pcix():
    return 'PCIX'


def pcie():
    return 'PCIE'


def usb3():
    pass


def networking():
    pass


def ssd():
    pass


def sata():
    pass


def space():
    pass


def boots():
    return 'Y'


def stable():
    pass


def cddvd():
    pass


def sra():
    return 'SRA'


def support():
    pass


sudocheck()
prereqcheck()
