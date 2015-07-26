Name:		libva
Version:	1.6.0
Release:	1%{?dist}
Summary:	Video Acceleration (VA) API for Linux
Group:		System Environment/Libraries
License:	MIT
URL:		http://freedesktop.org/wiki/Software/vaapi
Source0:	http://www.freedesktop.org/software/vaapi/releases/libva/libva-%{version}.tar.bz2
#Patch0:	firefox-crash-fix.patch

BuildRequires:	libudev-devel
BuildRequires:	libXext-devel
BuildRequires:	libXfixes-devel
BuildRequires:	libdrm-devel
BuildRequires:  libpciaccess-devel
BuildRequires:	mesa-libEGL-devel
BuildRequires:	mesa-libGL-devel
BuildRequires:	mesa-libGLES-devel
%{?_with_wayland:
BuildRequires:  wayland-devel
BuildRequires:  pkgconfig(wayland-client) >= 1
BuildRequires:  pkgconfig(wayland-server) >= 1
}
%{!?_with_wayland:
Obsoletes:  %{name}-wayland < %{version}-%{release}
}
# owns the %{_libdir}/dri directory
Requires:	mesa-dri-filesystem

%description
Libva is a library providing the VA API video acceleration API.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}%{_isa} = %{version}-%{release}
%{?_with_wayland:
Requires: %{name}-wayland%{_isa} = %{version}-%{release}
}
Requires:	pkgconfig

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	utils
Summary:	Tools for %{name} (including vainfo)
Group:		Development/Libraries
Requires:	%{name}%{_isa} = %{version}-%{release}

%description	utils
The %{name}-utils package contains tools that are provided as part
of %{name}, including the vainfo tool for determining what (if any)
%{name} support is available on a system.

%{?_with_wayland:
%package	wayland
Summary:	Wayland support for VA API
Group:		System Environment/Libraries
Requires:	%{name}%{_isa} = %{version}-%{release}

%description	wayland
The %{name}-wayland package contains libraries that are provided as part
of %{name}, to use with wayland.
}

%prep
%setup -q
#%patch0 -p1

%build
%configure --disable-static \
  --enable-glx \
%{?_with_wayland:--enable-wayland}

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -regex ".*\.la$" | xargs rm -f --


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING
%{?_with_wayland:
%exclude %{_libdir}/libva-wayland.so.*
}
%{_libdir}/libva*.so.*
# Keep these specific: if any new real drivers start showing up
# in libva, we need to know about it so they can be patent-audited
%{_libdir}/dri/dummy_drv_video.so

%files devel
%{_includedir}/va
%{_libdir}/libva*.so
%{_libdir}/pkgconfig/libva*.pc

%files utils
%{_bindir}/vainfo
%{_bindir}/loadjpeg
%{_bindir}/avcenc
%{_bindir}/h264encode
%{_bindir}/mpeg2vldemo
%{_bindir}/mpeg2vaenc
%{_bindir}/putsurface
%{_bindir}/jpegenc

%{?_with_wayland:
%files wayland
%{_libdir}/libva-wayland.so.*
%{_bindir}/putsurface_wayland
}

%changelog
* Sun Jul 26 2015 Jure Kobal <j.kobal@gmx.com> - 1.6.0-1
- Update to 1.6.0

* Fri Jun 20 2014 Elad Alfassa <elad@fedoraproject.org> - 1.2.1-3
- Apply upstream patch to fix a firefox crash (rhbz #1105890)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 27 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.2.1-1
- Update to 1.2.1
- Add mpeg2vaenc

* Wed Jun 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-1
- Update to 1.2.0
- Exclude mpeg2enc for now - namespace clash

* Fri Apr 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.1.1-2
- Switch Requires to mesa-dri-filesystem

* Wed Mar 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.1.1-1
- Update to 1.1.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.1.0-5
- Drop wayland support - Lead to suspicious crash
  to reintroduce later using alternates build for vainfo and libs.

* Thu Nov 15 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.1.0-4
- Fix condition rhbz#877059

* Sat Oct 06 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.1.0-3
- Update to official 1.1.0 release
- Enable Wayland support on f18 - add subpackage
- Clean spec file

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 01 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.1.0-1
- Update to 1.1.0 - VA-API version 0.33.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 03 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.15-1
- Update to 1.0.15
- Back to vanilla upstream sources - no backend are provided anymore

* Sun Aug 07 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.14-1
- Update to 1.0.14

* Fri Jun 10 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.13-2
- Add versioned requirement between main/utils

* Wed Jun 08 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.13-1
- Update to 1.0.13

* Fri Apr 08 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.12-1
- Update to 1.0.12

* Mon Feb 21 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.10-1
- Update to 1.0.10

* Tue Jan 25 2011 Adam Williamson <awilliam@redhat.com> - 1.0.8-1
- bump to new version
- fix modded tarball to actually not have i965 dir
- merge with the other spec I seem to have lying around somewhere

* Wed Nov 24 2010 Adam Williamson <awilliam@redhat.com> - 1.0.6-1
- switch to upstream from sds branch (sds now isn't carrying any very
  interesting changes according to gwenole)
- pull in the dont-install-test-programs patch from sds
- split out libva-utils again for multilib purposes
- drop -devel package obsolete/provides itself too

* Tue Nov 23 2010 Adam Williamson <awilliam@redhat.com> - 0.31.1-3.sds4
- drop obsoletes and provides of itself (hangover from freeworld)

* Tue Nov 23 2010 Adam Williamson <awilliam@redhat.com> - 0.31.1-2.sds4
- fix the tarball to actually remove the i965 code (duh)

* Thu Oct 7 2010 Adam Williamson <awilliam@redhat.com> - 0.31.1-1.sds4
- initial package (based on package from elsewhere by myself and Nic
  Chauvet with i965 driver removed)
