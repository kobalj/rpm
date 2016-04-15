Name:           nml
Version:        0.4.2
Release:        3%{?dist}
Summary:        NewGRF Meta Language compiler

License:        GPLv2+
URL:            http://dev.openttdcoop.org/projects/nml
Source0:        http://bundles.openttdcoop.org/nml/releases/%{version}/%{name}-%{version}.tar.gz
Patch0:         0001-pillow-Remove-deprecated-tostring-fromstring-call.patch

BuildRequires:  python3-devel python-pillow python-ply python3-setuptools
Requires:       python-pillow python-ply python3-setuptools

%description
A tool to compile nml files to grf or nfo files, making newgrf coding easier.


%prep
%setup -q
%patch0 -p1


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

gzip docs/nmlc.1
install -Dpm 644 docs/nmlc.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/nmlc.1.gz
rm docs/nmlc.1.gz

 
%files
%doc docs/*
%doc %{_mandir}/man1/nmlc.1.gz
%{_bindir}/nmlc
%{python3_sitearch}/nml*


%changelog
* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 28 2015 Felix Kaechele <heffer@fedoraproject.org> - 0.4.2-2
- fix calls to deprecated pillow functions

* Sun Oct 25 2015 Felix Kaechele <heffer@fedoraproject.org> - 0.4.2-1
- update to 0.4.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Felix Kaechele <heffer@fedoraproject.org> - 0.4.1-2
- add missing BuildRequires

* Mon May 18 2015 Felix Kaechele <heffer@fedoraproject.org> - 0.4.1-1
- update to 0.4.1
- remove version_foo variable (YAY!)

* Wed Feb 18 2015 Felix Kaechele <heffer@fedoraproject.org> - 0.4.0-1
- update to 0.4.0
- now uses Python 3
- is no longer noarch

* Mon Jun 30 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 0.3.1-2
- Replace python-setuptools-devel BR with python-setuptools

* Sat Jun 21 2014 Felix Kaechele <heffer@fedoraproject.org> - 0.3.1-1
- update to 0.3.1
- change Source0 URL / source dir name *again* (for the worse, le sigh)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Felix Kaechele <heffer@fedoraproject.org> - 0.3.0-1
- update to 0.3.0
- drop patch for pillow support (upstreamed)
- change Source0 URL / source dir name

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 14 2013 Felix Kaechele <heffer@fedoraproject.org> - 0.2.4-1
- update to 0.2.4
- patch for pillow support

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 11 2012 Felix Kaechele <heffer@fedoraproject.org> - 0.2.3-2
- add python-setuptools runtime requirement

* Thu Mar 29 2012 Felix Kaechele <heffer@fedoraproject.org> - 0.2.3-1
- initial spec
