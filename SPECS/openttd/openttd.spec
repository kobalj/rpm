# If we have a prerelease version we can define it here
#%%global prever RC1

Name:           openttd
Version:        1.6.0
Release:        1%{?prever}%{?dist}
Summary:        Transport system simulation game

Group:          Amusements/Games
License:        GPLv2
URL:            http://www.openttd.org
Source0:        http://binaries.openttd.org/releases/%{version}%{?prever:-%{prever}}/%{name}-%{version}%{?prever:-%{prever}}-source.tar.xz

BuildRequires:  desktop-file-utils, SDL-devel, libpng-devel, unzip, zlib-devel
BuildRequires:  fontconfig-devel, libtimidity-devel, libicu-devel, lzo-devel
BuildRequires:  freetype-devel, xz-devel, ccache, doxygen
Requires:       hicolor-icon-theme
Requires:       openttd-opengfx => 0.5.0

%description
OpenTTD is modeled after a popular transportation business simulation game
by Chris Sawyer and enhances the game experience dramatically. Many features
were inspired by TTDPatch while others are original.


%package docs
Summary:        Documentation for OpenTTD
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description docs
Development documentation for OpenTTD. Includes information on how to program
the AI.


%prep
%setup -q -n %{name}-%{version}%{?prever:-%{prever}}


%build
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
# not using the configure macro since this isn't really autotools so it
# doesn't eat all the argument rpm passes when using the configure
# macro
./configure \
        --prefix-dir= \
        --binary-dir=%{_bindir} \
        --data-dir=%{_datadir}/%{name} \
        --icon-dir=%{_datadir}/pixmaps \
        --icon-theme-dir=%{_datadir}/icons/hicolor \
        --man-dir=%{_mandir}/man6 \
        --menu-dir=%{_datadir}/applications \
        --doc-dir=%{_docdir} \
        --install-dir=$RPM_BUILD_ROOT \
        --disable-strip \
        --with-ccache \
        --enable-lto
make %{?_smp_mflags} VERBOSE=1


%install
make install VERBOSE=1

# Remove the installed docs - we will install subset of those
rm -rf $RPM_BUILD_ROOT%{_docdir}

# install documentation
install -dpm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/docs/
cp -r docs/* $RPM_BUILD_ROOT%{_datadir}/%{name}/docs/

desktop-file-install --dir=$RPM_BUILD_ROOT%{_datadir}/applications \
        --add-category=StrategyGame \
        media/openttd.desktop

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Ankur Sinha <ankursinha@fedoraproject.org> -->
<!--
EmailAddress: alberth@openttd.org
SentUpstream: 2014-09-25
-->
<application>
  <id type="desktop">openttd.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <summary>A highly detailed transport simulation game</summary>
  <description>
  <p>
      OpenTTD is a transport tycoon simulation game that enhances the
      original Transport Tycoon game developed by Chris Sawyer.
      The game includes road, air, train and naval transport with a large
      selection of industries and passenger services that need to be provided.
    </p>
  <p>
      The game can be played in both single and multiplayer modes where
      you compete with other transport companies to dominate the markets.
  </p>
  </description>
  <url type="homepage">http://www.openttd.org</url>
  <screenshots>
    <screenshot type="default">http://media.openttd.org/images/screens/1.4/02-opengfx-1920x1200.png</screenshot>
  <screenshot>http://media.openttd.org/images/screens/1.3/realgrowth.png</screenshot>
  </screenshots>
    <updatecontact>info@openttd.org</updatecontact>
</application>
EOF

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc COPYING changelog.txt known-bugs.txt readme.txt
%{_bindir}/%{name}
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man6/%{name}.6*
%{_datadir}/%{name}
%{_datadir}/pixmaps/%{name}.32.xpm
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%exclude %{_datadir}/%{name}/docs

%files docs
# These are really devel docs, but as we don't have -devel subpackage, we put it here
# Could be useful for people making graphics, AI scripts or translations
%{_datadir}/%{name}/docs/


%changelog
* Fri Apr 15 2016 Jure Kobal <kobal j AT gmail DOT com> - 1.5.3-01
- Rebuild for Centos7

* Sat Jan 02 2016 Felix Kaechele <heffer@fedoraproject.org> - 1.5.3-1
- update to 1.5.3

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 1.5.2-2
- rebuild for ICU 56.1

* Sat Oct 03 2015 Felix Kaechele <heffer@fedoraproject.org> - 1.5.2-1
- update to 1.5.2

* Tue Jul 28 2015 Felix Kaechele <heffer@fedoraproject.org> - 1.5.1-1
- update to 1.5.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.5.0-2
- Rebuilt for GCC 5 C++11 ABI change

* Sun Apr 05 2015 Felix Kaechele <heffer@fedoraproject.org> - 1.5.0-1
- update to 1.5.0
- remove compile patch, fixed upstream

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 1.4.4-3
- Add an AppData file for the software center

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 1.4.4-2
- rebuild for ICU 54.1

* Tue Oct 21 2014 Felix Kaechele <heffer@fedoraproject.org> - 1.4.4-1
- update to 1.4.4

* Tue Sep 23 2014 Felix Kaechele <heffer@fedoraproject.org> - 1.4.3-1
- update to 1.4.3

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 1.4.2-3
- rebuild for ICU 53.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 16 2014 Felix Kaechele <heffer@fedoraproject.org> - 1.4.2-1
- update to 1.4.2

* Sat Jun 21 2014 Felix Kaechele <heffer@fedoraproject.org> - 1.4.1-1
- update to 1.4.1
- change my e-mail in the changelogs

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 04 2014 Felix Kaechele <heffer@fedoraproject.org> - 1.4.0-1
- update to 1.4.0
- bump dependency on openttd-opengfx to 0.5.0

* Thu Feb 13 2014 Felix Kaechele <heffer@fedoraproject.org> - 1.3.3-2
- rebuild for new ICU

* Thu Dec 12 2013 Felix Kaechele <heffer@fedoraproject.org> - 1.3.3-1
- update to 1.3.3
- fixes CVE-2013-6411

* Sat Sep 21 2013 Felix Kaechele <heffer@fedoraproject.org> - 1.3.2-3
- another try at a rebuild to fix BZ#989786

* Fri Aug 02 2013 Felix Kaechele <heffer@fedoraproject.org> - 1.3.2-2
- rebuild for icu

* Sun Jul 28 2013 Felix Kaechele <heffer@fedoraproject.org> - 1.3.2-1
- update to 1.3.2

* Mon Jul 22 2013 David Tardon <dtardon@redhat.com> - 1.3.2-0.2.RC1
- rebuild for ICU ABI break

* Thu Jul 04 2013 Felix Kaechele <heffer@fedoraproject.org> - 1.3.2-0.1.RC1
- update to 1.3.2-RC1

* Wed May 22 2013 Felix Kaechele <heffer@fedoraproject.org> - 1.3.1-0.1.RC1
- update to the 1.3.1-RC1
- fixes compilation with F19+

* Mon Apr 08 2013 Felix Kaechele <heffer@fedoraproject.org> - 1.3.0-1
- update to 1.3.0

* Sat Mar 23 2013 Felix Kaechele <heffer@fedoraproject.org> - 1.3.0-0.1.RC3
- update to 1.3.0-RC3
- fixes compilation on F19+

* Fri Feb 08 2013 Jon Ciesla <limburgher@gmail.com> - 1.2.3-2
- libicu rebuild.

* Sat Dec 15 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.2.3-1
- update to 1.2.3

* Sat Aug 18 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.2.2-1
- fixes CVE-2012-3436
- many other bugfixes

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.2.1-1
- update to 1.2.1

* Mon Apr 23 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.2.0-2
- rebuild for new icu

* Sun Apr 15 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.2.0-1
- update to stable 1.2.0

* Tue Apr 03 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.2.0-0.1.RC4
- Update to 1.2.0-RC4
- builds in F17 and rawhide again

* Sun Jan 15 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.1.5-1
- update to 1.1.5
- fixes CVE-2012-0049 (bz #782179)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.1.3-2
- Rebuild for new libpng

* Sun Sep 18 2011 Felix Kaechele <heffer@fedoraproject.org> - 1.1.3-1
- update to 1.1.3
- fixes CVE-2011-3341, CVE-2011-3342 and CVE-2011-3343

* Fri Sep 09 2011 Felix Kaechele <heffer@fedoraproject.org> - 1.1.2-2
- rebuild for new icu

* Mon Aug 29 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 1.1.2-1
- update to 1.1.2
- drop definition of buildroot, defattr and clean stage

* Sun Jun 12 2011 Felix Kaechele <heffer@fedoraproject.org> - 1.1.1-1
- update to 1.1.1

* Tue Apr 05 2011 Felix Kaechele <heffer@fedoraproject.org> - 1.1.0-2
- add BR xz-devel

* Tue Apr 05 2011 Felix Kaechele <heffer@fedoraproject.org> - 1.1.0-1
- update to 1.1.0
- cleaned up configure arguments
- enabled GCC's Link Time Optimization (LTO)

* Mon Mar 07 2011 Caolán McNamara <caolanm@redhat.com> - 1.0.5-3
- rebuild for icu 4.6

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 21 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.0.5-1
- 1.0.5
- fixes CVE-2010-4168 Denial of service (server/client) via invalid read
- switched to using the XZ tarball

* Sat Sep 18 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.0.4-1
- new upstream release

* Tue Aug 03 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.0.3-1
- update to final 1.0.3
- fixes various and desync bugs

* Sat Jul 24 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.0.3-0.1.RC1
- update to 1.0.3-RC1
- contains fixes for a remote DoS described in CVE-2010-2534

* Sun Jun 20 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.0.2-1
- update to 1.0.2
- contains bugfixes and translation updates

* Sat May 01 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- fixes CVE-2010-0401, CVE-2010-0402, CVE-2010-0406

* Fri Apr 02 2010 Caolán McNamara <caolanm@redhat.com> - 1.0.0-2
- rebuild for icu 4.4

* Thu Apr 01 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.0.0-1
- update to final release

* Thu Mar 18 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.0.0-0.6.RC3
- update to RC3

* Thu Mar 04 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.0.0-0.5.RC2
- 1.0.0-RC2 bugfix release

* Wed Feb 24 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.0.0-0.4.RC1
- update to RC1

* Fri Feb 05 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.0.0-0.3.beta4
- 1.0.0-beta4

* Thu Jan 21 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.0.0-0.2.beta3
- 1.0.0-beta3

* Sat Jan 16 2010 Felix Kaechele <heffer@fedoraproject.org>
- 1.0.0-beta2

* Sat Jan 02 2010 Felix Kaechele <heffer@fedoraproject.org> - 0.7.5-1
- 0.7.5 stable release
- fixes CVE-2009-4007

* Thu Dec 17 2009 Felix Kaechele <heffer@fedoraproject.org> - 0.7.5-0.1.rc1
- bump to 0.7.5-RC1
- omitting 0.7.4 because it has a bug

* Sat Oct 10 2009 Alexey Torkhov <atorkhov@gmail.com> - 0.7.3-1
- New upstream release 0.7.3

* Sun Aug 23 2009 Felix Kaechele <heffer@fedoraproject.org> - 0.7.2-1
- new upstream release 0.7.2

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Felix Kaechele <heffer@fedoraproject.org> - 0.7.1-1
- upstream 0.7.1

* Sun May 31 2009 Felix Kaechele <heffer@fedoraproject.org> - 0.7.1-0.4.rc2
- disable allegro due to performance problems

* Fri May 29 2009 Felix Kaechele <heffer@fedoraproject.org> - 0.7.1-0.3.rc2
- updated icon cache scriptlets

* Thu May 28 2009 Felix Kaechele <heffer@fedoraproject.org> - 0.7.1-0.2.rc2
- 0.7.1-RC2
- build docs from source

* Sat May 16 2009 Felix Kaechele <heffer@fedoraproject.org> - 0.7.1-0.1.rc1
- updated to 0.7.1-RC1

* Sat Apr 11 2009 Felix Kaechele <felix at fetzig dot org> - 0.7.0-1
- upstream 0.7.0
- added docs subpackage

* Sun Mar 29 2009 Felix Kaechele <felix at fetzig dot org> - 0.7.0-0.3.rc2
- 0.7.0-RC2
- dropped Patch0 since this does not reflect the behaviour that is intended
  by upstream. See http://bugs.openttd.org/task/2756

* Sat Mar 21 2009 Felix Kaechele <felix at fetzig dot org> - 0.7.0-0.2.rc1
- updated to RC1
- removed all references to possible trademarks
- added patch to ignore a missing sample.cat

* Mon Mar 09 2009 Alexey Torkhov <atorkhov@gmail.com> - 0.7.0-0.1.beta1
- Doing big cleanup of package:
- Dropping subpackages
- Drop .desktop sources in favour of one bundled
- Drop server menu entry - one can start server from game menu
- Drop suspicious data_patch (what was it needed for?)
- Cleanup macro usage
- Drop version from freetype build dep
- Correcting dirs in configure call: icons paths, disable duplicate shared dir,
  correct doc dir

- And adding few improvements:
- Using VERBOSE when doing make
- Adding libicu to build requires
- Add icons theme require
- Drop installation instructions from docs
- Use ccache (should speedup the local and mock builds)
- Change source url to canonical one

* Sun Jan 11 2009 Felix Kaechele <felix at fetzig dot org> - 0.6.3-3
- even more improvements made

* Sun Jan 11 2009 Felix Kaechele <felix at fetzig dot org> - 0.6.3-2
- incorporated suggestions made by reviewers

* Wed Dec 31 2008 Felix Kaechele <felix at fetzig dot org> - 0.6.3-1
- Initial build based on the SPEC by Peter Hanecak (http://hany.sk/~hany/RPM/)
