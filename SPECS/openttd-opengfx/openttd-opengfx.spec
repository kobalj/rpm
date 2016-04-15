%global realname opengfx
#global prever   alpha6

Name:           openttd-opengfx
Version:        0.5.3
Release:        1%{?prever:.%{prever}}%{?dist}
Summary:        OpenGFX replacement graphics for OpenTTD

Group:          Amusements/Games
License:        GPLv2
URL:            http://dev.openttdcoop.org/projects/opengfx
Source0:        http://bundles.openttdcoop.org/opengfx/releases/%{version}%{?prever:-%{prever}}/%{realname}-%{version}%{?prever:-%{prever}}-source.tar.xz

BuildArch:      noarch

BuildRequires:  gimp grfcodec nml
Requires:       openttd


%description
OpenGFX is an open source graphics base set for OpenTTD which can completely
replace the TTD base set. The main goal of OpenGFX therefore is to provide a
set of free base graphics which make it possible to play OpenTTD without
requiring the (copyrighted) files from the TTD CD. This potentially increases
the OpenTTD fan base and makes it a true free game (with "free" as in both
"free beer" and "free speech").

As of version 0.2.0 OpenGFX has a full set of sprites. Future versions will aim
to improve the graphics. 


%prep
%setup -q -n %{realname}-%{version}%{?prever:-%{prever}}-source 

%build
make grf _V=


%install
make install _V= UNIX2DOS= INSTALL_DIR=$RPM_BUILD_ROOT%{_datadir}/openttd/data


%check
cp %{realname}-%{version}.check.md5 %{realname}-%{version}.md5
make check


%files
%doc docs/
%{_datadir}/openttd/data/*


%changelog
* Sun Oct 25 2015 Felix Kaechele <heffer@fedoraproject.org> - 0.5.3-1
- update to 0.5.3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Felix Kaechele <heffer@fedoraproject.org> - 0.5.2-1
- update to 0.5.2
- Makefile.local is replaced by command line variables

* Sat Jun 21 2014 Felix Kaechele <heffer@fedoraproject.org> - 0.5.1-1
- update to 0.5.1
- upstream now only provides an xz tarball so change Source0 to that

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 04 2014 Felix Kaechele <heffer@fedoraproject.org> - 0.5.0-1
- update to 0.5.0

* Sun Dec 15 2013 Felix Kaechele <heffer@fedoraproject.org> - 0.4.7-1
- update to 0.4.7
- drop patch, it was upstreamed

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 23 2013 Felix Kaechele <heffer@fedoraproject.org> - 0.4.6.1-3
- fix gcc 4.8 patch

* Sat Mar 23 2013 Felix Kaechele <heffer@fedoraproject.org> - 0.4.6.1-2
- fix compilation on F19+
- specfile cleanups

* Thu Mar 14 2013 Felix Kaechele <heffer@fedoraproject.org> - 0.4.6.1-1
- update to 0.4.6.1
- remove unix2dos usage during compilation of docs
- enable verbosity

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 02 2012 Felix Kaechele <heffer@fedoraproject.org> - 0.4.5-1
- update to 0.4.5

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 19 2012 Felix Kaechele <heffer@fedoraproject.org> - 0.4.4-1
- update to 0.4.4
- use clean-gfx target to build completely from source

* Thu Mar 29 2012 Felix Kaechele <heffer@fedoraproject.org> - 0.4.3-1
- update to 0.4.3

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 23 2011 Felix Kaechele <heffer@fedoraproject.org> - 0.3.7-1
- updated river sprites (0.3.6)
- added new sprites for nightly versions of OpenTTD

* Sat Sep 03 2011 Felix Kaechele <heffer@fedoraproject.org> - 0.3.5-1
- update 0.3.5
- many bugfixes
- reworked aircarft sprites

* Sun Jun 12 2011 Felix Kaechele <heffer@fedoraproject.org> - 0.3.4-1
- update to 0.3.4
- switch to xz tarball
- updated description

* Mon Apr 04 2011 Felix Kaechele <heffer@fedoraproject.org> - 0.3.3-1
- bump version

* Wed Feb 09 2011 Felix Kaechele <heffer@fedoraproject.org> - 0.3.2-1
- update to new upstream release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 11 2010 Felix Kaechele <heffer@fedoraproject.org> - 0.3.1-1
- new upstream release
- contains mostly packaging fixes and a fix for the load sprite
- removed empty sample.cat, openttd now gives a warning and offers
  to download a sound set
- sprites are complete as of 0.3.0

* Sun May 09 2010 Felix Kaechele <heffer@fedoraproject.org> - 0.2.4-1
- mainly fixes for train alignment
- now relying on 'make check' for data integrity checks

* Mon Mar 29 2010 Felix Kaechele <heffer@fedoraproject.org> - 0.2.2-1
- bugfix release 0.2.2
- major fixes to houses and their alignment
- re-worked maglev and monorail vehicles
- translations into multiple languages

* Sat Jan 02 2010 Felix Kaechele <felix@fetzig.org> - 0.2.1-1
- upstream bugfix release

* Fri Dec 11 2009 Felix Kaechele <felix@fetzig.org> - 0.2.0-1
- update to 0.2.0
- cleaned up docs

* Sat Oct 10 2009 Alexey Torkhov <atorkhov@gmail.com> - 0.1.1-2
- Correct generation of grfs, using nforenum

* Sat Oct 10 2009 Alexey Torkhov <atorkhov@gmail.com> - 0.1.1-1
- New upstream release 0.1.1
- Check md5sums of resulting files

* Sun Aug 23 2009 Felix Kaechele <heffer@fedoraproject.org> - 0.1.0-0.1.alpha6
- new upstream release

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.5.alpha4.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 28 2009 Felix Kaechele <heffer@fedoraproject.org> - 0-0.4.alpha4.2
- added md5 check

* Tue Apr 14 2009 Felix Kaechele <heffer@fedoraproject.org> - 0-0.3.alpha4.2
- now compiles from source

* Sun Mar 29 2009 Felix Kaechele <heffer@fedoraproject.org> - 0-0.2.alpha4.2
- improved macro usage
- touch sample.cat

* Sat Mar 21 2009 Felix Kaechele <heffer@fedoraproject.org> - 0-0.1.alpha4.2
- initial build

