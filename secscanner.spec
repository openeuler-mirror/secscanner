%define name secScanner
%define version 1.2
%define release 0
%define os_version %(source /etc/os-release; echo ${VERSION})
%define os_id %(source /etc/os-release; echo ${ID})

Summary: System secure check and enhancement tool for system of Linux
Name: %{name}
Version: %{version}
Release: %{release}
License: MulanPSL-2.0
Group: Applications/System
URL: https://gitee.com/openeuler/secscanner
#Distribution: openEuler 22.03
Vendor: China Mobile (Suzhou) Software Technology Co., Ltd.
Packager: pengyuan_yewu@cmss.chinamobile.com
Provides: secscanner


BuildArch: noarch
BuildRoot: %{_builddir}/%{name}-root
#install dependence

BuildRequires: python3-pip
BuildRequires: python3

Requires: rpmdevtools
Requires: python3
Requires: chkrootkit
Requires: aide

%if 0%{?openEuler}
Requires: python3-psutil
Requires: python3-beautifulsoup4
Requires: python3-requests
Requires: python3-sqlalchemy
%endif

Source0: %{name}-%{version}.tar.gz

%description
Operating System Security Scanning Tool

%prep
%setup -q

#exit 0

%build
exit 0

%install
#install -p -m 755 %{SOURCE0} %{buildroot}
#install -p -m 755 %{_builddir}/%{name}-%{version} %{buildroot}/opt/

mkdir -p %{buildroot}/opt/secScanner/
cp -a %{_builddir}/%{name}-%{version}/* %{buildroot}/opt/secScanner/
if [ "%{os_id}" = "bclinux" ]; then
   pip3 install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
fi

#keep the secscanner file in /usr/bin
mkdir -p %{buildroot}/usr/bin
#create symbolic links
ln -snf /opt/secScanner/secscanner.py %{buildroot}/usr/bin/secscanner
#create man file
gzip -c %{buildroot}/opt/secScanner/secscanner.8 > %{buildroot}/opt/secScanner/secscanner.8.gz
mkdir -p %{buildroot}/usr/share/man/man8/
mv %{buildroot}/opt/secScanner/secscanner.8.gz %{buildroot}/usr/share/man/man8/
#create secscanner.conf in /etc/
mkdir -p %{buildroot}/etc/secScanner
mv %{buildroot}/opt/secScanner/secscanner.cfg %{buildroot}/etc/secScanner/secscanner.cfg
#record the file and dir properties
mkdir -p %{buildroot}/etc/secscanner.d/
#copy service file in /usr/lib/systemd/system/
mkdir -p %{buildroot}/usr/lib/systemd/system/
cp -p %{buildroot}/opt/secScanner/secScanner/services/service_file/* %{buildroot}/usr/lib/systemd/system/
cp -p %{buildroot}/opt/secScanner/secScanner/services/timer_file/* %{buildroot}/usr/lib/systemd/system/
#exit 0

%post


%clean
[ -d "$RPM_BUILD_ROOT" ] && rm -rf $RPM_BUILD_ROOT
exit 0

%files
%defattr(-,root,root)
/opt/secScanner/
/usr/bin/secscanner
/usr/share/man/man8/secscanner.8.gz
/etc/secScanner/secscanner.cfg
/etc/secscanner.d
/usr/lib/systemd/system/

%changelog
* Fri Mar 22 2024 pengyuan <pengyuan@cmss.chinamobile.com> 1.2-0
- modify subprocess func and add error prompts when entering commands

* Tue Mar 12 2024 pengyuan <pengyuan@cmss.chinamobile.com> 1.1-0
- fix bugs for S15
- add Python installation dependency on local software packages 

* Fri Mar 1 2024 pengyuan <pengyuan@cmss.chinamobile.com> 1.1-0
- Up to release 1.1
- add services func 
- add services and timers for secaid and sechkrootkit
- add service commands, including on/off/status

*Thu Jan 18 2024 pengyuan <pengyuan@cmss.chinamobile.com> 1.0-0
- Release 1.0
- modify some bugs

*Mon Nov 20 2023 pengyuan <pengyuan@cmss.chinamobile.com> 0.1-1
- up to release 0.1-1
- first complete version

*Mon Aug 14 2023 pengyuan <pengyuan@cmss.chinamobile.com> 0.1-0
- Fix Security Reinforcement Item Execution Mode
- Adjust the Command Line

*Fri Jun 30 2023 pengyuan <pengyuan@cmss.chinamobile.com> 0.1-0
- secscanner release 0.1-0
