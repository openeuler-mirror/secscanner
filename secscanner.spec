%define name secScanner
%define version 1.1
%define release 0


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

#BuildRequires: python3




Requires: rpmdevtools
Requires: python3
#Requires: python3-devel
Requires: chkrootkit
Requires: aide

#Requires: python3-psutil
#Requires: python3-beautifulsoup4
#Requires: python3-requests
#Requires: python3-sqlalchemy

Source0: %{name}-%{version}.tar.gz

Source100: beautifulsoup4-4.12.3-py3-none-any.whl
Source101: certifi-2024.2.2-py3-none-any.whl
Source102: charset_normalizer-2.0.12-py3-none-any.whl
Source103: idna-3.6-py3-none-any.whl
Source104: importlib_metadata-4.8.3-py3-none-any.whl
Source105: psutil-5.9.8-cp36-abi3-manylinux_2_12_x86_64.manylinux2010_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl
Source106: greenlet-2.0.2-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
Source107: requests-2.27.1-py2.py3-none-any.whl
Source108: soupsieve-2.3.2.post1-py3-none-any.whl
Source109: SQLAlchemy-1.4.52-cp36-cp36m-manylinux1_x86_64.manylinux2010_x86_64.manylinux_2_12_x86_64.manylinux_2_5_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl
Source110: typing_extensions-4.1.1-py3-none-any.whl
Source111: urllib3-1.26.18-py2.py3-none-any.whl
Source112: zipp-3.6.0-py3-none-any.whl


%description
Operating System Security Scanning Tool

%prep
%setup -q

#exit 0

%build
#pip3 install -r requirements.txt
#pip3 install psutil sqlalchemy requests
exit 0

%install
#install -p -m 755 %{SOURCE0} %{buildroot}
#install -p -m 755 %{_builddir}/%{name}-%{version} %{buildroot}/opt/

mkdir -p %{buildroot}/opt/secScanner/
cp -a %{_builddir}/%{name}-%{version}/* %{buildroot}/opt/secScanner/
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
