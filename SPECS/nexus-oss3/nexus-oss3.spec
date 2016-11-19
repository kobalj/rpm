%global pkgname nexus

Summary: Nexus manages software “artifacts” required for development, deployment, and provisioning.
Name: nexus3
Version: 3.1.0
Release: 04
License: AGPL
Group: unknown
URL: http://nexus.sonatype.org/
Source0: %{pkgname}-%{version}-%{release}-unix.tar.gz
Source1: nexus-oss3.service
Source2: nexus-oss3.conf.tmp
BuildRoot: %{_tmppath}/%{pkgname}-%{version}-%{release}-root
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel
AutoReqProv: no

BuildArch:      noarch
BuildRequires:  java-headless >= 1:1.8.0
Requires:  java-headless >= 1:1.8.0

%define __os_install_post %{nil}
%define debug_package %{nil}

%description
A package repository

%prep
%setup -q -n %{pkgname}-%{version}-%{release}

%build

%pre
/usr/bin/getent passwd nexus3 || /usr/sbin/useradd -r -d /var/lib/nexus3 -s /bin/bash nexus3

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/%{name}
mv * $RPM_BUILD_ROOT/usr/share/%{name}
mv .install4j $RPM_BUILD_ROOT/usr/share/%{name}

arch=$(echo "%{_arch}" | sed -e 's/_/-/')

# Remove not needed files
rm -r $RPM_BUILD_ROOT/usr/share/%{name}/bin/contrib

# Link config files
mkdir -p $RPM_BUILD_ROOT/etc/
ln -sf /usr/share/%{name}/etc $RPM_BUILD_ROOT/etc/%{name}

# Path log dir
mkdir -p $RPM_BUILD_ROOT/var/log/%{name}
sed -i -e 's/..\/sonatype-work\/nexus3\/log/\/var\/log\/nexus3/' $RPM_BUILD_ROOT/usr/share/%{name}/bin/nexus.vmoptions

# Patch work dir
sed -i -e 's/..\/sonatype-work\/nexus3/\/var\/lib\/nexus3/' $RPM_BUILD_ROOT/usr/share/%{name}/bin/nexus.vmoptions
mkdir -p $RPM_BUILD_ROOT/var/lib/%{name}
mkdir -p $RPM_BUILD_ROOT/var/lib/%{name}/log

# Patch user
sed -i -e "s/#run_as_user=\"\"/run_as_user='nexus3'/" $RPM_BUILD_ROOT/usr/share/%{name}/bin/nexus.rc

# install service script
install -p -D -m 0644 %{SOURCE1} \
    $RPM_BUILD_ROOT/usr/lib/systemd/system/%{name}.service

install -p -D -m 0644 %{SOURCE2} \
    $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/%{name}.conf


%postun
/usr/sbin/userdel nexus3

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc
/usr/share/%{name}
/usr/lib/systemd/system/%{name}.service
/usr/lib/tmpfiles.d/%{name}.conf

#/etc/rc.d/init.d/nexus
%attr(-,nexus3,nexus3) /etc/%{name}
%attr(-,nexus3,nexus3) /var/lib/%{name}
%attr(-,nexus3,nexus3) /var/log/%{name}
%attr(-,nexus3,nexus3) /usr/share/%{name}

%config(noreplace) /usr/share/nexus3/etc/fabric/ehcache.xml
%config(noreplace) /usr/share/nexus3/etc/fabric/elasticsearch.yml
%config(noreplace) /usr/share/nexus3/etc/fabric/hazelcast.xml
%config(noreplace) /usr/share/nexus3/etc/fabric/orientdb-distributed.json
%config(noreplace) /usr/share/nexus3/etc/fabric/orientdb-security.json
%config(noreplace) /usr/share/nexus3/etc/jetty/jetty-http-redirect-to-https.xml
%config(noreplace) /usr/share/nexus3/etc/jetty/jetty-http.xml
%config(noreplace) /usr/share/nexus3/etc/jetty/jetty-https.xml
%config(noreplace) /usr/share/nexus3/etc/jetty/jetty-requestlog.xml
%config(noreplace) /usr/share/nexus3/etc/jetty/jetty.xml
%config(noreplace) /usr/share/nexus3/etc/jetty/nexus-web.xml
%config(noreplace) /usr/share/nexus3/etc/karaf/config.properties
%config(noreplace) /usr/share/nexus3/etc/karaf/custom.properties
%config(noreplace) /usr/share/nexus3/etc/karaf/java.util.logging.properties
%config(noreplace) /usr/share/nexus3/etc/karaf/jmx.acl.cfg
%config(noreplace) /usr/share/nexus3/etc/karaf/jre.properties
%config(noreplace) /usr/share/nexus3/etc/karaf/org.apache.felix.fileinstall-deploy.cfg
%config(noreplace) /usr/share/nexus3/etc/karaf/org.apache.karaf.features.cfg
%config(noreplace) /usr/share/nexus3/etc/karaf/org.apache.karaf.jaas.cfg
%config(noreplace) /usr/share/nexus3/etc/karaf/org.apache.karaf.kar.cfg
%config(noreplace) /usr/share/nexus3/etc/karaf/org.apache.karaf.log.cfg
%config(noreplace) /usr/share/nexus3/etc/karaf/org.apache.karaf.management.cfg
%config(noreplace) /usr/share/nexus3/etc/karaf/org.apache.karaf.service.acl.command.cfg
%config(noreplace) /usr/share/nexus3/etc/karaf/org.apache.karaf.shell.cfg
%config(noreplace) /usr/share/nexus3/etc/karaf/org.apache.karaf.shell.cfg
%config(noreplace) /usr/share/nexus3/etc/karaf/profile.cfg
%config(noreplace) /usr/share/nexus3/etc/karaf/shell.init.script
%config(noreplace) /usr/share/nexus3/etc/karaf/startup.properties
%config(noreplace) /usr/share/nexus3/etc/karaf/system.properties
%config(noreplace) /usr/share/nexus3/etc/logback/logback-access.xml
%config(noreplace) /usr/share/nexus3/etc/logback/logback.xml
%config(noreplace) /usr/share/nexus3/etc/nexus-default.properties
%config(noreplace) /usr/share/nexus3/bin/nexus.vmoptions
%config(noreplace) /usr/share/nexus3/bin/nexus.rc

%changelog
* Sat Nov 19 2016 Jure Kobal <kobal j AT gmail DOT com> - 3.1.0-04
- Update to new major releas of nexus 3.1.0-04

* Thu Aug 25 2016 Jure Kobal <kobal j AT gmail DOT com> - 2.13.0-01
- Update to 2.13.0-01

* Fri Apr 15 2016 Jure Kobal <kobal j AT gmail DOT com> - 2.12.1-01
- Update to 2.12.1-01

* Sun Jan 03 2016 Jure Kobal <kobal j AT gmail DOT com> - 2.12.0-01
- Updated to 2.12.0-01
- Added support for systemd on CentOS 7

* Tue Jul 21 2015 Julio Gonzalez <git@juliogonzalez.es> - 2.11.4-01
- Update to 2.11.4-01

* Fri Jun 26 2015 Julio Gonzalez <git@juliogonzalez.es> - 2.11.3-01
- Update to last version available
- Nexus will now listen at 8081 (this can be modified at
  /etc/nexus/nexus.properties)
- Nexus runs now without as system user, not as root
- Remove jdk dependency (no virtual package at CentOS 7)

* Thu Dec 22 2011 Jens Braeuer <braeuer.jens@googlemail.com> - 1.9.2.3-1
- Initial packaging.
- For now nexus will run as root and listen to port 80

