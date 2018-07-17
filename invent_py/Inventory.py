#!/usr/bin/python

import subprocess
import os
import re

IS_DIG_DEC = re.compile(r'\d+\.?\d*')  # Is an integer or decimal


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
    prerequisites = ['dmidecode', 'util-linux', 'ethtool', 'usbutils', 'gptfdisk']
    for i in range(len(prerequisites)):
        rpm = subprocess.Popen(('rpm', '-qa', '--last'), stdout=subprocess.PIPE)
        try:
            output = subprocess.check_output(('grep', '-iw', prerequisites[i]), stdin=rpm.stdout)
        except Exception as e:
            output = None
        rpm.wait()
        if output is None:
            print('Installing dependency: ' + prerequisites[i])
            os.system('zypper -n install ' + prerequisites[i])
        else:
            print('Dependency ' + prerequisites[i] + ' is already satisfied')


def asset():
    return 'ASSET'


def hostname():
    """
    Determines the hostname of the machine via three methods
    :return: Hostname of current machine
    """
    host_a = str(subprocess.check_output(('hostname', '-s'))).rstrip()
    host_b1 = subprocess.Popen(('uname', '-n'), stdout=subprocess.PIPE)
    host_b2 = subprocess.check_output(('sed', 's/[.].*$//'), stdin=host_b1.stdout)
    host_b = str(host_b2).rstrip()
    host_c1 = open('/etc/hostname')
    host_c = host_c1.readline().rstrip()

    if host_a is not None:
        return host_a
    elif host_b is not None:
        return host_b
    elif host_c is not None:
        return host_c
    else:
        return "---"


def pcode():
    return 'PCODE'


def mm():
    return 'MM'


def sdp():
    return 'SDP'


def serialnumber():
    """
    Uses dmidecode to find system serial number
    :return: System serial number
    """
    serial = str(subprocess.check_output(('dmidecode', '-s', 'system-serial-number'))).rstrip()

    if serial is not None:
        if any(c.isalpha() for c in serial):
            return serial
    else:
        return "---"


def makemodel():
    """
    Determines the CPU architecture-type
    :return: Returns the make and model of the CPU
    """
    compinfo = subprocess.Popen(('cat', '/proc/cpuinfo'), stdout=subprocess.PIPE)
    comparch = subprocess.Popen(('grep', '-m', '1', '-i', 'model name'), stdin=compinfo.stdout, stdout=subprocess.PIPE)
    compinfo.stdout.close()
    compmodel = subprocess.check_output(('sed', 's/.*: //'), stdin=comparch.stdout)
    comparch.stdout.close()
    make = str(compmodel).rstrip()

    if make is not None:
        return make
    else:
        return "---"


def vendor():
    """
    Determines the brand of CPU used
    :return: CPU type
    """
    vendorlscpu = subprocess.Popen('lscpu', stdout=subprocess.PIPE)
    vendorgrep = subprocess.Popen(('grep', '-i', 'Vendor ID'), stdin=vendorlscpu.stdout, stdout=subprocess.PIPE)
    vendorlscpu.stdout.close()
    vendorsed1 = subprocess.Popen(('sed', 's/.*: //'), stdin=vendorgrep.stdout, stdout=subprocess.PIPE)
    vendorgrep.stdout.close()
    vendorsed2 = subprocess.check_output(('sed', '-e', 's/[ \t]*//'), stdin=vendorsed1.stdout)
    vendorsed1.stdout.close()

    vendorname = str(vendorsed2).rstrip()

    if vendorname == "GenuineIntel":
        return 'Intel'
    elif vendorname == "AuthenticAMD":
        return 'AMD'
    elif vendorname == "":
        return "---"
    else:
        return vendorname


def codename():
    """
    Determines the product name of the actual motherboard/machine that it is used on
    :return: Returns the system's codename
    """
    sysman = str(subprocess.check_output(('dmidecode', '-s', 'system-manufacturer'))).rstrip() + " "
    sysprodname = str(subprocess.check_output(('dmidecode', '-s', 'system-product-name'))).rstrip() + " "
    sysver = str(subprocess.check_output(('dmidecode', '-s', 'system-version'))).rstrip()

    # Checks for incomplete information

    sysinfo = [sysman, sysprodname, sysver]

    for i in range(len(sysinfo)):
        if not any(c.isalpha for c in sysinfo[i]):
            sysinfo[i] = ""

    sysname = sysman + sysprodname + sysver

    if sysname is not None:
        return str(sysname)
    else:
        return "---"


def cpuspeed():
    """
    Determines the maximum speed of the processor
    :return: float that represents cpu speed in GHz
    """
    speeds = []

    # Method 1: lscpu
    lscpulscpu = subprocess.Popen('lscpu', stdout=subprocess.PIPE)
    lscpugrep = subprocess.Popen(('grep', '-i', 'CPU max MHz'), stdin=lscpulscpu.stdout, stdout=subprocess.PIPE)
    lscpulscpu.stdout.close()
    lscpuspeed = str(subprocess.check_output(('sed', 's/.*: //'), stdin=lscpugrep.stdout)).rstrip().lstrip()
    lscpugrep.stdout.close()

    if IS_DIG_DEC.match(str(lscpuspeed)):  # Verifies that the input is an integer or float.
        lscpuspeed = float(lscpuspeed) / 1000
        lscpuspeed = format(lscpuspeed, '.2f')
    else:
        lscpuspeed = "---"
    speeds.append(lscpuspeed)

    # Method 2: dmidecode
    dmidmi = subprocess.Popen('dmidecode', stdout=subprocess.PIPE)
    dmigrep = subprocess.Popen(('grep', '-m', '1', 'Max Speed'), stdin=dmidmi.stdout, stdout=subprocess.PIPE)
    dmidmi.stdout.close()
    dmised = str(subprocess.check_output(('sed', 's/.*: //'), stdin=dmigrep.stdout)).rstrip()
    dmigrep.stdout.close()
    dmispeed = re.sub("[^0-9]", "", dmised)
    dmispeed = float(dmispeed) / 1000
    dmispeed = format(dmispeed, '.2f')
    speeds.append(dmispeed)

    # Method 3.1 cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq:
    syscat = str(subprocess.check_output(('cat', '/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq'))).rstrip()
    if IS_DIG_DEC.match(str(syscat)):
        sysspeed = float(syscat) / 1000000
        sysspeed = format(sysspeed, '.2f')
    else:
        sysspeed = "---"
    speeds.append(sysspeed)

    # Method 3.2 cat/sys/devices/system/cpu/cpu/cpufreq/cpuinfo_max_freq:
    cpucat = str(subprocess.check_output(('cat', '/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq'))).rstrip()
    if IS_DIG_DEC.match(str(cpucat)):
        cpuspeeds = float(cpucat) / 1000000
        cpuspeeds = format(cpuspeeds, '.2f')
    else:
        cpuspeeds = "---"
    speeds.append(cpuspeeds)

    # Take the highest value out of all possible speeds and return it
    filterlist = []
    for i in range(len(speeds)):
        if IS_DIG_DEC.match(str(speeds[i])):
            filterlist.append(speeds[i])

    return max(filterlist)


def sockets():
    """
    Determines how many threads the cpu has
    :return: An integer that represents the number of physical cpus
    """
    lscpusocket = subprocess.Popen('lscpu', stdout=subprocess.PIPE)
    grepsocket = subprocess.Popen(('grep', '-i', 'socket(s)'), stdin=lscpusocket.stdout, stdout=subprocess.PIPE)
    lscpusocket.stdout.close()
    sedsocket = str(subprocess.check_output(('sed', 's/.*: //'), stdin=grepsocket.stdout)).rstrip().lstrip()
    grepsocket.stdout.close()

    if sedsocket is not None:
        return sedsocket
    else:
        return "---"


def threads():
    """
    Determines how many threads the cpu has
    :return: An integer that shows how many cores are on the system
    """
    lscputhread = subprocess.Popen('lscpu', stdout=subprocess.PIPE)
    grepthread = subprocess.Popen(('grep', '-m', '1', '-i', 'cpu(s)'), stdin=lscputhread.stdout, stdout=subprocess.PIPE)
    lscputhread.stdout.close()
    sedthread = str(subprocess.check_output(('sed', 's/.*: //'), stdin=grepthread.stdout)).rstrip().lstrip()
    grepthread.stdout.close()

    if sedthread is not None:
        return sedthread
    else:
        return "---"


def hyperthreading():
    """
    Determines if the computer has more than one cpu
    :return: Yes or no, and a special null case
    """
    if int(threads()) > 1:
        return 'Y'
    elif int(threads()) == 1:
        return 'N'
    else:
        return '---'


def cpucores():
    """
    Determines the amount of cores / cpu
    :return: An integer that represents how many threads per core there are
    """
    try:
        return int(threads())/int(sockets())
    except TypeError:
        return '---'


def ram():
    """
    Determines the amount of RAM in the system (this method is not very accurate)
    :return: Integer that represents the amount of RAM in the system
    """
    catdividend = subprocess.Popen(('cat', '/proc/meminfo'), stdout=subprocess.PIPE)
    grepdividend = subprocess.Popen(('grep', '-i', 'memtotal'), stdin=catdividend.stdout, stdout=subprocess.PIPE)
    catdividend.stdout.close()
    seddividend = subprocess.Popen(('sed', 's/.*: //'), stdin=grepdividend.stdout, stdout=subprocess.PIPE)
    grepdividend.stdout.close()
    sed2dividend = str(subprocess.check_output(('sed', 's/[^0-9]*//g'), stdin=seddividend.stdout)).rstrip().lstrip()
    seddividend.stdout.close()
    dividend = int(sed2dividend)
    divisor = 1048576
    quotient = dividend/divisor

    try:
        if (quotient % 2) == 1:
            quotient += 1
        elif (quotient % 2) == 0:
            quotient += 2
        return quotient
    except TypeError:
        return '---'


def virttech():
    """
    Determines if cpu virtualization technology is supported on the System
    :return: Yes or no
    """
    catvirt = subprocess.Popen(('cat', '/proc/cpuinfo'), stdout=subprocess.PIPE)
    grepvirt = subprocess.Popen(('grep', '-m', '1', 'flags'), stdin=catvirt.stdout, stdout=subprocess.PIPE)
    catvirt.stdout.close()
    try:
        grep2virt = str(subprocess.check_output(('grep', '-oE', 'vmx|svm'), stdin=grepvirt.stdout)).rstrip()
        grepvirt.stdout.close()
    except Exception as e:
        grepvirt.stdout.close()
        grep2virt = None

    if grep2virt is not None:
        return 'Y'
    else:
        return "---"


def vtd():
    return 'VTD'


def hap():
    """
    Determines if the processor is capable of hardware assisted paging
    :return: String that is either 'Y' or 'N'
    """
    cathap = subprocess.Popen(('cat', '/proc/cpuinfo'), stdout=subprocess.PIPE)
    grephap = subprocess.Popen(('grep', '-m', '1', 'flag'), stdin=cathap.stdout, stdout=subprocess.PIPE)
    cathap.stdout.close()
    try:
        grep2hap = subprocess.check_output(('grep', '-o', 'ept'), stdin=grephap.stdout)
        grephap.stdout.close()
    except Exception as e:
        grep2hap = None
        grephap.stdout.close()
    if grep2hap is not None:
        return 'Y'
    else:
        return 'N'


def sriov():
    return 'SRIOV'


def numa():
    pass


def efi():
    """
    Determines if the system has EFI capabilities
    :return: 'Y' or 'N' based on if the /sys/firmware/efi dir exists
    """
    lsefi = subprocess.Popen(('ls', '/sys/firmware'), stdout=subprocess.PIPE)
    try:
        grepefi = subprocess.check_output(('grep', '-oi', 'efi'), stdin=lsefi.stdout)
        lsefi.stdout.close()
    except Exception as e:
        grepefi = None
        lsefi.stdout.close()
    if grepefi is not None:
        return 'Y'
    else:
        return 'N'


def pci():
    return 'PCI'


def pcix():
    return 'PCIX'


def pcie():
    return 'PCIE'


def usb3():
    """
    Determines how many USB 3.0 slots are on the machine
    :return: An int that defines the number of USB 3.0 slots
    """
    lsusbusb = subprocess.Popen('lsusb', stdout=subprocess.PIPE)
    grepusb = subprocess.Popen(('grep', '-ow', '3.0'), stdin=lsusbusb.stdout, stdout=subprocess.PIPE)
    lsusbusb.stdout.close()
    wcusb = str(subprocess.check_output(('wc', '-l'), stdin=grepusb.stdout)).rstrip()
    grepusb.stdout.close()
    return wcusb


def networking():
    """
    Determines how many of each type of ethernet port exists in the system (not counting SYS MGMT ports) and their speed
    :return: An array where 0=100Mb, 1=1Gb, 2=10Gb, and 3=40Gb
    """
    lseth = subprocess.Popen(('ls', '/sys/class/net'), stdout=subprocess.PIPE)
    fortyg = 0
    teng = 0
    oneg = 0
    oneh = 0
    ethdevices = []
    try:
        grepeth = str(subprocess.check_output(('grep', '-E', 'eth|en'), stdin=lseth.stdout)).rstrip()
        lseth.stdout.close()
    except Exception as e:
        grepeth = None
        lseth.stdout.close()
    if grepeth is not None:
        if "\n" in grepeth:
            ethdevices = grepeth.splitlines()
        else:
            ethdevices.append(grepeth)
        for i in range(len(ethdevices)):
            for fn in ('40000base', '10000base', '1000base', '100base'):
                try:
                    ethspeed = subprocess.Popen(('ethtool', str(ethdevices[i])), stdout=subprocess.PIPE)
                    grepspeed = subprocess.check_output(('grep', '-m', '1', '-o', fn), stdin=ethspeed.stdout)
                    ethspeed.stdout.close()
                    if fn is '40000base':
                        fortyg += 1
                        break
                    elif fn is '10000base':
                        teng += 1
                        break
                    elif fn is '1000base':
                        oneg += 1
                        break
                    elif fn is '100base':
                        oneh += 1
                        break
                    else:
                        exit(code=1)
                except Exception as e:
                    continue
    ethspeeds = [oneh, oneg, teng, fortyg]
    return ethspeeds


def ssd():
    """
    Determines how many SSDs exist in a system
    :return: An int that describes the number of SSDs in the system
    """
    ssds = 0
    issda = subprocess.Popen(('ls', '/sys/block'), stdout=subprocess.PIPE)
    try:
        grepissda = str(subprocess.check_output(('grep', '-w', 'sda'), stdin=issda.stdout)).rstrip()
        issda.stdout.close()
    except Exception as e:
        grepissda = None
        issda.stdout.close()
    if grepissda is not None:
        sddev = []
        lsdev = str(subprocess.check_output('ls -d /sys/block/sd*', shell=True)).rstrip()
        if '\n' in lsdev:
            sddev = lsdev.splitlines()
        else:
            sddev.append(lsdev)
        for i in range(len(sddev)):
            if str(subprocess.check_output(('cat', str(sddev[i]) + '/queue/rotational'))).rstrip() is '0':
                ssds += 1
    else:
        return '---'
    return ssds


def sata():
    """
    Determines how many of the devices on the system use the SATA protocol
    :return: An int representing how many devices use SATA
    """
    satadevs = 0
    issda = subprocess.Popen(('ls', '/sys/block'), stdout=subprocess.PIPE)
    try:
        grepissda = str(subprocess.check_output(('grep', '-w', 'sda'), stdin=issda.stdout)).rstrip()
        issda.stdout.close()
    except Exception as e:
        grepissda = None
        issda.stdout.close()
    if grepissda is not None:
        satadev = []
        lssata = subprocess.Popen(('ls', '-g', '/dev/disk/by-path'), stdout=subprocess.PIPE)
        grepsata = subprocess.Popen(('grep', '-v', 'part'), stdin=lssata.stdout, stdout=subprocess.PIPE)
        lssata.stdout.close()
        grep2sata = str(subprocess.check_output(('grep', '../sd'), stdin=grepsata.stdout)).rstrip()
        grepsata.stdout.close()
        if '\n' in grep2sata:
            satadev = grep2sata.splitlines()
        else:
            satadev.append(grep2sata)
        for i in range(len(satadev)):
            isata = subprocess.Popen(('echo', str(satadev[i])), stdout=subprocess.PIPE)
            try:
                grepata = str(subprocess.check_output(('grep', '-wo', 'ata'), stdin=isata.stdout)).rstrip()
                isata.stdout.close()
            except Exception as e:
                grepata = None
                isata.stdout.close()
            if grepata is not None:
                satadevs += 1
    else:
        return '---'
    return satadevs


def space():
    """
    Determines the amount of available storage space on the system
    :return: Float that represents total storage space
    """
    totalspace = 0.0
    issda = subprocess.Popen(('ls', '/sys/block'), stdout=subprocess.PIPE)
    try:
        grepissda = str(subprocess.check_output(('grep', '-w', 'sda'), stdin=issda.stdout)).rstrip()
        issda.stdout.close()
    except Exception as e:
        grepissda = None
        issda.stdout.close()
    if grepissda is not None:
        stodev = []
        lsstodev = subprocess.Popen('ls -d /dev/sd*', stdout=subprocess.PIPE, shell=True)
        grepstodev = str(subprocess.check_output(('grep', '-v', '[0-9]'), stdin=lsstodev.stdout)).rstrip()
        lsstodev.stdout.close()
        if '\n' in grepstodev:
            stodev = grepstodev.splitlines()
        else:
            stodev.append(grepstodev)
        for i in range(len(stodev)):
            devspace = subprocess.Popen(('sgdisk', '--print', str(stodev[i])), stdout=subprocess.PIPE)
            grepspace = subprocess.Popen(('grep', '-m', '1', '[0-9].'), stdin=devspace.stdout, stdout=subprocess.PIPE)
            devspace.stdout.close()
            sedspace = subprocess.Popen(('sed', '-e', 's/^.*,//g'), stdin=grepspace.stdout, stdout=subprocess.PIPE)
            grepspace.stdout.close()
            sed2space = str(subprocess.check_output(('sed', 's/[^0-9.]*//g'), stdin=sedspace.stdout)).rstrip()
            sedspace.stdout.close()
            totalspace += float(sed2space)
    return totalspace


def boots():
    return 'Y'


def stable():
    return 'STABLE'


def cddvd():
    """
    Determines if the machine is bootable by CD/DVD
    :return: 'Y' or 'N' based on the existence of the drives
    """
    iscdvd = subprocess.Popen(('ls', '/dev'), stdout=subprocess.PIPE)
    try:
        grepcdvd = str(subprocess.check_output(('grep', '-i', 'cdrom\|cdrw\|dvd\|dvdrw'), stdin=iscdvd.stdout)).rstrip()
        iscdvd.stdout.close()
    except Exception as e:
        grepcdvd = None
        iscdvd.stdout.close()
    if grepcdvd is not None:
        return 'Y'
    else:
        return 'N'


def sra():
    return 'SRA'


def support():
    """
    Determines if machine is still supported by Intel
    :return: 'N/A' or 'SUPPORT', this cannot be seen in the interior
    """
    if vendor() is not "Intel":
        return 'N/A'
    else:
        return 'SUPPORT'


def cpufamily():
    """
    Determines the family number of a certain type of cpu
    :return: Int indicative of the family number
    """
    try:
        fam = subprocess.Popen(('grep', '-m', '1', 'family', '/proc/cpuinfo'), stdout=subprocess.PIPE)
        sedfam = str(subprocess.check_output(('sed', 's/.*: //'), stdin=fam.stdout)).rstrip()
        fam.stdout.close()
        return sedfam
    except Exception as e:
        return '---'


def cpumodel():
    """
    Determines the model number of a certain type of cpu
    :return: Int indicative of the model number
    """
    try:
        mod = subprocess.Popen(('grep', '-m', '1', 'model', '/proc/cpuinfo'), stdout=subprocess.PIPE)
        sedmod = str(subprocess.check_output(('sed', 's/.*: //'), stdin=mod.stdout)).rstrip()
        mod.stdout.close()
        return sedmod
    except Exception as e:
        return '---'


def cpustepping():
    """
    Determines the stepping number of a certain type of cpu
    :return: Int indicative of the stepping number
    """
    try:
        step = subprocess.Popen(('grep', '-m', '1', 'stepping', '/proc/cpuinfo'), stdout=subprocess.PIPE)
        sedstep = str(subprocess.check_output(('sed', 's/.*: //'), stdin=step.stdout)).rstrip()
        step.stdout.close()
        return sedstep
    except Exception as e:
        return '---'


def cpumicrocode():
    pass


sudocheck()
# prereqcheck()
hostname()
serialnumber()
makemodel()
vendor()
codename()
cpuspeed()
sockets()
threads()
hyperthreading()
cpucores()
ram()
virttech()
hap()
numa()
efi()
usb3()
networking()
ssd()
sata()
space()
cddvd()
support()
cpufamily()
print(cpumodel())
