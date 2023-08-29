%define name secScanner
%define version 0.1
%define release 0


Summary: System secure check and enhancement tool for system of Linux
Name: %{name}
Version: %{version}
Release: %{release}
License: MulanPSL2
Group: Applications/System
URL: https://gitee.com/openeuler/secscanner
Distribution: openEuler 22.03
Vendor: China Mobile (Suzhou) Software Technology Co., Ltd.
Packager: pengyuan_yewu@cmss.chinamobile.com
Provides: secscanner


BuildArch: noarch
BuildRoot: %{_builddir}/%{name}-root
#install dependence
Requires: rpmdevtools
#Requires: chkrootkit
Source0:%{name}-%{version}.tar.gz


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
#keep the bse file in /usr/bin
mkdir -p %{buildroot}/usr/bin
#create symbolic links
ln -snf /opt/secScanner/secscanner.py %{buildroot}/usr/bin/
#create man file
gzip -c %{buildroot}/opt/secScanner/secscanner.8 > %{buildroot}/opt/secScanner/secscanner.8.gz
mkdir -p %{buildroot}/usr/share/man/man8/
mv %{buildroot}/opt/secScanner/secscanner.8.gz %{buildroot}/usr/share/man/man8/
#create secscanner.conf in /etc/
mkdir -p %{buildroot}/etc/secScanner
mv %{buildroot}/opt/secScanner/secscanner.cfg %{buildroot}/etc/secScanner/secscanner.cfg
#record the file and dir properties
mkdir -p %{buildroot}/etc/secscanner.d/

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

%changelog
*Mon Aug 14 2023 pengyuan <pengyuan@cmss.chinamobile.com> 0.1-0
- Fix Security Reinforcement Item Execution Mode
- Adjust the Command Line

*Fri Jun 30 2023 pengyuan <pengyuan@cmss.chinamobile.com> 0.1-0
- secscanner release 0.1-0
