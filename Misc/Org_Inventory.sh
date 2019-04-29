#!/bin/bash
# Authored by: Christopher Kitras
# Date of first rev: 2018-06-21
# Last revision: 2018-06-26

  # Declare global vars
  VERSION="0.0.1"

  echo 'Welcome to the Inventory Shell script v'$VERSION

  # Check to see if user is root or has sudo privileges
  if [[ $(id -u) != 0 ]];then
    echo "You must run this script as root or under sudo"
    exit 1
  fi

  IS_NUM='^[0-9]+$'

  # Install prerequisites
  declare -a arr=(dmidecode util-linux ethtool usbutils gptfdisk bc)
  for i in "${arr[@]}"
  do
    if [[  $(rpm -qa --last | grep -iw $i) == "" ]];then
      echo "Installing dependency: $i"
      $(zypper -n install "$i")
    else
      echo "Dependency $i already satisfied"
    fi
  done
  echo ""
  echo "SYSTEM INFORMATION"
  echo "------------------"
  # Determine asset tag number for the machine
  ASSET="EVAL no."

  # Determine the hostname of the machine
  a=$(hostname -s)
  b=$(uname -n | sed 's/[.].*$//')
  c=$(cat /etc/hostname | sed 's/[.].*$//')

  if [ "$a" != "" ];then
    MACH_HOST="$a"
  elif [ "$b" != "" ];then
    MACH_HOST="$b"
  elif [ "$c" != "" ];then
    MACH_HOST="$c"
  else
    MACH_HOST="No name found"
  fi
  echo "Hostname: $MACH_HOST"
  # Platform Processor/ Pcode: return whitespace because the number is only found on physical machine
  PCODE="PCODE"

  # MM#: return whitespace because the number is only found on physical machine
  MM="MM"

  # Software Development Products: return whitespace because the number is only found on physical machine
  SDP="SDP"

  # Determine the System Serial number
  a=$(dmidecode -s system-serial-number)

  if [ "$a" != "" ];then
    SYS_SERIAL="$a"
  else
    SYS_SERIAL="No serial no. found"
  fi

  echo "System Serial: $SYS_SERIAL"
  # Determine the Make/Model of the machine
  a=$(cat /proc/cpuinfo | grep -m 1 -i 'model name' | sed 's/.*: //')

  if [ "$a" != "" ];then
    MAKE_MODEL="$a"
  else
    MAKE_MODEL="No make/model found"
  fi

  echo "Make/Model: $MAKE_MODEL"
  # Determine the Vendor of the machine
  a=$(lscpu | grep -i 'Vendor ID' | sed 's/.*: //' | sed -e 's/^[ \t]*//')

  if [ "$a" == "GenuineIntel" ];then
    VENDOR="Intel"
  elif [ "$a" == "AuthenticAMD" ];then
    VENDOR="AMD"
  else
    VENDOR="$a"
  fi

  echo "Vendor: $VENDOR"
  # Determine the Model/Codename of the machine
  a_man=$(dmidecode -s system-manufacturer)
  a_pro_name=$(dmidecode -s system-product-name)
  a_ver_num=$(dmidecode -s system-version)

  CODENAME="$a_man $a_pro_name $a_ver_num"

  if [[ $CODENAME == "" ]];then
    CODENAME="No codename found"
  fi

  echo "Codename: $CODENAME"
  # Determine the maximum speed of the processor\
  a_dividend=$(lscpu | grep -i 'CPU max MHz' | sed 's/.*: //' | sed -e 's/^[ \t]*//')
  d_dividend=$(dmidecode | grep -m 1 "Max Speed" | sed 's/.*: //' | sed 's/[^0-9]*//g')
  a_divisor=1000
  if [[ $a_dividend != "" ]];then
    a=$(echo "$a_dividend/$a_divisor" | bc -l)
    a=$(printf "%0.2f\n" $a)
    SPEED="$a"
  elif [[ $d_dividend != "" ]];then
    d=$(echo "$d_dividend/$a_divisor" | bc -l)
    d=$(printf "%0.2f\n" $d)
    SPEED="$d"
  else
    b_dividend=$(cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq)
    if [[ $b_dividend != "" ]];then
      if [[ $b_dividend =~ $IS_NUM ]];then
        b_divisor=1000000
        b=$(echo "$b_dividend/$b_divisor" | bc -l)
        b=$(printf "%0.2f\n" $b)
        SPEED="$b"
      fi
    else
      b_dividend=$(cat /sys/devices/system/cpu/cpu/cpufreq/cpuinfo_max_freq)
      if [[ $b_dividend != "" ]];then
        if [[ $b_dividend =~ $IS_NUM ]];then
          b_divisor=1000000
          b=$(echo "$b_dividend/$b_divisor" | bc -l)
          b=$(printf "%0.2f\n" $b)
          SPEED="$b"
        fi
      else
        SPEED="No max CPU speed found"
      fi
    fi
  fi

  echo "CPU Max Speed (GHz): $SPEED"
  # Determine the number of sockets on a machine
  a=$(lscpu | grep -i 'socket(s)' | sed 's/.*: //' | sed -e 's/^[ \t]*//')

  SOCKETS="$a"

  echo "Sockets: $SOCKETS"
  # Determines how many threads the CPU has
  a=$(lscpu | grep -m 1 -i 'cpu(s)' | sed 's/.*: //' | sed -e 's/^[ \t]*//')

  THREADS="$a"

  echo "Threads: $THREADS"
  # Determines if the computer has more than one CPU
  if [[ "$THREADS" -gt 1 ]];then
    HT="Y"
  elif [[ "$THREADS" -eq 1 ]];then
    HT="N"
  else
    HT="The correct amount of CPU threads could not be determined"
  fi

  echo "Hyperthreading: $HT"
  # Determines the amount of cores / cpu
  a=$((THREADS / SOCKETS))
  CPCPU="$a"

  echo "Cores per CPU: $CPCPU"
  # Determines the amount of RAM in a System
  a_dividend=$(cat /proc/meminfo | grep -i memtotal | sed 's/.*: //' | sed -e 's/^[ \t]*//' | sed 's/[^0-9]*//g')
  a_divisor=1048576
  a_quotient=$((a_dividend / a_divisor))
  if [[ $((a_quotient % 2)) -eq 1 ]];then
    a_quotient=$((a_quotient + 1))
  elif [[ $((a_quotient % 2)) -eq 0 ]];then
    a_quotient=$((a_quotient + 2))
  else
    echo 'You might want to check your math, bro.'
  fi

  RAM="$a_quotient"

  echo "RAM: $RAM"
  # Determines if cpu virtualization technology is supported in System
  a_intel=$(cat /proc/cpuinfo | grep -m 1 flag | grep vmx)
  a_amd=$(cat /proc/cpuinfo | grep -m 1 flag | grep svm)

  if [[ $a_amd != "" || $a_intel != "" ]];then
    VT="Y"
  else
    VT="N"
  fi

  echo "Virtualization: $VT"
  # Determines if the system has either VT-d, IOMMU, or AMD-Vi technology
  VTD="VTD"

  # Determines if machine supports hardware assisted paging
  a=$(cat /proc/cpuinfo | grep -m 1 flag | grep ept)

  if [[ "$a" != "" ]];then
    HAP="Y"
  else
    HAP="N"
  fi

  echo "Hardware Assisted Paging: $HAP"
  # Determines if machine supports SR_IOV
  SRIOV="SRIOV"

  # Determines if machine supports NUMA
  a=$(dmesg | grep -i numa)

  if [[ $a != "" ]];then
    NUMA="Y"
  else
    NUMA="N"
  fi

  echo "NUMA: $NUMA"
  # Determines if the motherboard has EFI capabilities
  a=$(ls /sys/firmware | grep -i efi)

  if [[ $a == "efi" ]];then
    EFI="Y"
  elif [[ $a == "" ]];then
    EFI="N"
  else
    EFI="Rare exception found, further investigation required"
  fi

  echo "EFI: $EFI"
  # Determines how mnay PCI slots are on motherboard
  PCI="PCI"

  # Determines how many PCI-X slots are on motherboard
  PCIX="PCIX"

  # Determines how many PCI-Express slots are on motherboard
  PCIE="PCIE"

  # Determines how many USB 3.0 slots are on machine
  a=$(lsusb | grep -ow '3.0')

  if [[ $a == "3.0" ]];then
    isUSB="Y"
  elif [[ $a == "" ]]; then
    isUSB="N"
  else
    USB="Rare exception found, further investigation required"
  fi

  if [[ $isUSB -eq "Y" ]];then
    USB=$(lsusb | grep -ow '3.0' | wc -l)
  else
    USB=0
  fi

  echo "USB 3.0: $USB"
  # NETWORKING INFO PART:

  FORTYG=0
  TENG=0
  ONEG=0
  ONEH=0

  declare -a arr=($(ls /sys/class/net | grep -i 'eth\|en'))
  if [[ $(command -v ethtool) != "" ]];then
    for i in "${arr[@]}"
    do
      if [[ $(ethtool "$i" | grep -m 1 -o 40000base) ]]; then
        ((FORTYG++))
      elif [[ $(ethtool "$i" | grep -m 1 -o 10000base) ]]; then
        ((TENG++))
      elif [[ $(ethtool "$i" | grep -m 1 -o 1000base) ]]; then
        ((ONEG++))
      elif [[ $(ethtool "$i" | grep -m 1 -o 100base) ]]; then
        ((ONEH++))
      else
        ONEH="There is was an error with 1+ of the devices"
      fi
    done
  else
    FORTYG="???"
    TENG="???"
    ONEG="???"
    ONEH="???"
  fi

  echo "Ethernet Ports: "
  echo "  40Gb: $FORTYG"
  echo "  10Gb: $TENG"
  echo "  1Gb: $ONEG"
  echo "  100Mb: $ONEH"
  # Determine how many SSDs are in the machine
  SSD=0

  if [[ $(ls /sys/block | grep -w sda) == "sda" ]]; then
    declare -a arr=($(ls -d /sys/block/sd*))

    for i in "${arr[@]}"
    do
      if [[ $(cat $i/queue/rotational) -eq 0 ]]; then
        ((SSD++))
      fi
    done
  else
    SSD="???"
  fi

  echo "SSDs: $SSD"
  # Determine how many storage devices are using the SATA connection protocol
  SATA=0

  if [[ $(ls /sys/block | grep -w sda) == "sda" ]]; then
    OLD_IFS=$IFS
    IFS=$'\n'
    declare -a arr=($(ls -g /dev/disk/by-path/ | grep -v part | grep '../sd'))
    for i in "${arr[@]}"
    do
      if [[ $(echo "$i" | grep -wo ata) == "ata" ]]; then
        ((SATA++))
      fi
    done
  else
    SATA="???"
  fi
  IFS=$OLD_IFS

  echo "SATA storage devices: $SATA"
  # Determine the total storage space on system
  SPACE=0

  if [[ $(ls /sys/block | grep -w sda) == "sda" ]]; then
    OLD_IFS=$IFS
    IFS=$'\n'
    declare -a arr=($(ls -d /dev/sd* | grep -v '[0-9]'))
    for i in "${arr[@]}"
    do
    a=$(sgdisk --print "$i" | grep -m 1 '[0-9].' | sed -e 's/^.*,//g' | sed 's/[^0-9.]*//g')
    SPACE=$(echo "$SPACE + $a" | bc -l)
  done
  else
    SPACE="???"
  fi
  IFS=$OLD_IFS

  echo "Total disk space: $SPACE"
  # Determines if machine boots or not
  BOOTS="Y" #This will always be yes because while the script is running, so will the System

  # Determines if the machine is stable and apt for rigorous use
  STABLE="STABLE"

  # Determines if the machine is bootable by CD/DVD
  if [[ $(ls /dev | grep -i 'cdrom\|cdrw\|dvd\|dvdrw') != "" ]]; then
    CDDVD="Y"
  else
    CDDVD="N"
  fi

  echo "CD/DVD: $CDDVD"
  echo "------------------"
  echo ""
  # Determines if the machine is accessible by Serial Remote Access
  SRA="SRA"

  # Determines if machine is still supported by Intel
  if ! [[ $VENDOR == "Intel" ]];then
    SUPPORT="N/A"
  else
    SUPPORT="SUPPORT"
  fi

  # Export's machine's info to line in spreadsheet
  echo "$ASSET, $MACH_HOST, $PCODE, $MM, $SDP, $SYS_SERIAL, $CODENAME, $VENDOR, $MAKE_MODEL, $SPEED, $SOCKETS, $CPCPU, $HT, $THREADS, $RAM, $VT, $VTD, $HAP, $SRIOV, $NUMA, $EFI, $PCI, $PCIX, $PCIE, $USB, $ONEH, $ONEG, $TENG, $FORTYG, $SSD, $SATA, $SPACE, $BOOTS, $STABLE, $CDDVD, $SRA, $SUPPORT"  >> Inventory.csv
  # echo "$ASSET, $MACH_HOST, $PCODE, $MM, $SDP, $SYS_SERIAL, $MAKE_MODEL, $VENDOR, $CODENAME, $SPEED, $SOCKETS, $CPCPU, $HT, $THREADS, $RAM, $VT, $VTD, $HAP, $SRIOV, $NUMA, $EFI, $PCI, $PCIX, $PCIE, $USB, $ONEH, $ONEG, $TENG, $FORTYG, $SSD, $SATA, $SPACE, $BOOTS, $STABLE, $CDDVD, $SRA, $SUPPORT"
