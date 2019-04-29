#
# Spec file for the Inventory Script to be run for the Virtualization Lab
#
Summary: A script that will keep the inventories of the virtualization lab up-to-date
Name: Inventory
Version: 1.0
Release: 1
License: GPL-3.0-or-later
Group: Development/Libraries/Python
Source0: %{name}-%{version}.tar.gz
Source1: xlutils-2.0.0.tar.gz
URL: https://github.com/ckglxe95/Inventory
Distribution: SUSE Enterprise Linux
BuildRequires: python
Requires: python2-pip
Requires: dmidecode
Requires: util-linux
Requires: ethtool
Requires: usbutils
Requires: gptfdisk
Requires: numactl
Requires: python
Requires: python2-xlwt
Requires: python2-xlrd
Requires: python-setuptools


%description
This is a simple script that returns certain system values from host machine
as to more easily maintain the inventories of the virtualization lab

%prep
%setup -q

%build

python2 -m compileall %{name}.py

cat <<\EOT > %{name}
#!/bin/sh
if [[ $(pip2 list | grep 'xlutils') == "" ]];then
	pip2 install xlutils --no-cache-dir
fi
/usr/bin/env python2 /usr/%{_lib}/%{name}/%{name}.py $@
EOT

%install

# Define the macro for SLES-11-SP4
%if 0%{?suse_version} < 1110 || 0%{?suse_version} == 1110
%define buildroot /home/abuild/rpmbuild/BUILDROOT
install -d %{buildroot}
%endif

install -d %{buildroot}%{_bindir}
install -d %{buildroot}/usr/%{_lib}/%{name}
install -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 0755 %{name}.py %{buildroot}/usr/%{_lib}/%{name}/%{name}.py

%files
%dir /usr/%{_lib}/%{name}
%{_bindir}/%{name}
/usr/%{_lib}/%{name}/%{name}.py

%changelog

