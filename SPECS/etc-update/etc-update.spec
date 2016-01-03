Name:           etc-update
Version:        1.0
Release:        2%{?dist}
Summary:        CLI to interactively merge *.rpmnew
License:        GPL
Group:          Applications/System
URL:            https://wiki.gentoo.org/wiki/Handbook:X86/Portage/Tools

Source0:        etc-update-1.0.tar.gz
Patch0:         etc-update-centos_port.patch

%description
etc-update is a tool to help merging changes made in config files during updates.

%prep
%setup 
%patch0 -p0 

#%build

%install
install -D -m 700 etc-update.gentoo $RPM_BUILD_ROOT/%{_sbindir}/%{name}
install -D -m 644 etc-update.conf $RPM_BUILD_ROOT/%{_sysconfdir}/etc-update.conf

%files
%{_sbindir}/%{name}
%config(noreplace) %{_sysconfdir}/etc-update.conf

%changelog
* Sun Jan 04 2016 Jure Kobal <kobalj AT gmail DOT com> 1.0.0-2
- Fix in exec script (commit 80fd57b)

* Fri Nov 05 2015 Jure Kobal <kobalj AT gmail DOT com> 1.0.0-1
- Initial CentOS package
