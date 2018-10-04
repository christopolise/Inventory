#
# Spec file for the Inventory Script to be run for the Virtualization Lab
#
Summary: A script that will keep the inventory for the virtualization lab up-to-date
Name: inventory
Version: 1.0
Release: 1
License: ---
Group: Unspecified
Source: https://github.com/ckglxe95/Inventory/archive/master.zip
URL: https://github.com/ckglxe95/Inventory
Distribution: SUSE Enterprise Linux
Vendor: I'm not making any money off of this ¯\_(ツ)_/¯
Packager: Chris Kitras <ckitras@suse.com>
Requires: dmidecode, util-linux, ethtool, usbutils, gptfdisk, numactl

%description
This is a simple script that returns certain system values from host machine
as to more easily maintain the inventory in the virtualization lab.


%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 inventory %{buildroot}%{_bindir}/inventory
mkdir -p %{_datadir}/inventory
install -m 755 Inventory.py %{_datadir}/inventory/Inventory.py

%files
%{_bindir}/inventory
%{_datadir}/inventory/Inventory.py

