Name:    robocut
Summary: A program to cut SVG with CC220-20 and Silhouette SD/Cameo
Group: Productivity/Graphics/Other
Version: 1.0.11
Release: 1%{?dist}

License: GPL-3.0+
URL:     https://robocut.org/
Source0: robocut-%{version}.tar.gz


BuildRequires: qt5-qtbase-devel
BuildRequires: libusbx-devel

%description
Robocut is a simple graphical program to allow you to cut graphics with a
Graphtec Craft Robo 2 Vinyl Cutter model CC220-20 and Sihouette SD, among other devices.

It can read SVG files produced by Inkscape, but it should also work with other
SVG files.  Unlike the official programs, Robocut can run on Linux and probably
Mac OS X.

Inside the “examples” folder there is also a registration marks template fully
functional (yes, the Silhouette Cameo is able to recognize registration marks
also under Robocut, just put the page with the arrow pointing toward the
plotter and align the sheet with the top left corner of the cutting mat).

Authors

Tim Hutt, Markus Schulz

%prep
%setup -q

%build
%{qmake_qt5} Robocut.pro
make

%install
install -D robocut                    $RPM_BUILD_ROOT/usr/bin/robocut
install -m 0644 -D images/robocut.xpm $RPM_BUILD_ROOT/usr/share/pixmaps/robocut.xpm
install -d                            $RPM_BUILD_ROOT/usr/share/robocut/examples
install -m 0644 examples/*      $RPM_BUILD_ROOT/usr/share/robocut/examples
install -m 0644 -D robocut.1 $RPM_BUILD_ROOT/usr/share/man/man1/robocut.1
install -d	$RPM_BUILD_ROOT/usr/share/applications
install -m 0644 -D robocut.desktop $RPM_BUILD_ROOT/usr/share/applications/robocut.desktop


install -d $RPM_BUILD_ROOT/usr/share/icons/hicolor/16x16/apps
install -m 0644 -D icons/16x16/apps/robocut.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/16x16/apps/robocut.png
install -d $RPM_BUILD_ROOT/usr/share/icons/hicolor/22x22/apps
install -m 0644 -D icons/22x22/apps/robocut.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/22x22/apps/robocut.png
install -d $RPM_BUILD_ROOT/usr/share/icons/hicolor/24x24/apps
install -m 0644 -D icons/24x24/apps/robocut.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/24x24/apps/robocut.png
install -d $RPM_BUILD_ROOT/usr/share/icons/hicolor/32x32/apps
install -m 0644 -D icons/32x32/apps/robocut.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/32x32/apps/robocut.png
install -d $RPM_BUILD_ROOT/usr/share/icons/hicolor/64x64/apps
install -m 0644 -D icons/64x64/apps/robocut.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/64x64/apps/robocut.png
install -d $RPM_BUILD_ROOT/usr/share/icons/hicolor/scalable/apps
install -m 0644 -D icons/scalable/apps/robocut.svg $RPM_BUILD_ROOT/usr/share/icons/hicolor/scalable/apps/robocut.svg


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/robocut.desktop

%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%files
%defattr(-,root,root)
#%doc readme.txt changelog

%_bindir/*
%_datadir/pixmaps/*
%dir %_datadir/robocut
%_datadir/robocut/*
%{_datadir}/applications/robocut.desktop
%{_datadir}/icons/hicolor/*/*/*
%_mandir/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Jul 22 2018 Jure Kobal <kobal j AT gmail DOT com> - 1.0.11-1
- Initial build with version 1.0.11
