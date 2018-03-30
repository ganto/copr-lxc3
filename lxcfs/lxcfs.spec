Name:       lxcfs
Version:    3.0.0
Release:    0.1%{?dist}
Summary:    FUSE filesystem for LXC

License:    ASL 2.0
URL:        https://linuxcontainers.org
Source0:    https://github.com/lxc/lxcfs/archive/%{name}-%{version}.tar.gz
Patch0:     lxcfs-2.0.5-Fix-systemd-unit-directory.patch
Patch1:     lxcfs-2.0.5-Fix-fusermount-path.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: help2man
BuildRequires: libtool
BuildRequires: pkgconfig
BuildRequires: pkgconfig(fuse)
BuildRequires: systemd

%{?systemd_requires}

AutoProv:      no

%description
LXCFS is a simple userspace filesystem designed to work
around some current limitations of the Linux kernel.

Specifically, it's providing two main things

- A set of files which can be bind-mounted over their
  /proc originals to provide CGroup-aware values.
- A cgroupfs-like tree which is container aware. The
  code is pretty simple, written in C using libfuse
  and glib.

%prep
%autosetup -n %{name}-%{version} -p1

%build
autoreconf --force --install
# RHEL still defaults to sysvinit
%configure --with-init-script=systemd
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}
install -d -m 0755 %{buildroot}%{_localstatedir}/lib/%{name}/
rm -f %{buildroot}%{_libdir}/%{name}/liblxcfs.la

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root)
%doc AUTHORS
%license COPYING
%{_bindir}/*
%{_datadir}/lxc
%{_datadir}/%{name}
%{_libdir}/%{name}
%{_mandir}/man1/*
%{_unitdir}/%{name}.service
%dir %{_localstatedir}/lib/%{name}

%changelog
* Mon Feb 05 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.0.8-0.2
- Fix systemd scriptlets
- Fix removal of static library

* Wed Oct 25 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.0.8-0.1
- Update to 2.0.8.

* Wed May 17 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.0.7-1
- Version bump to lxcfs-2.0.7

* Thu Feb 02 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.0.6-2
- Add patches to fix fusermount path and swap size reporting

* Mon Jan 30 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.0.6-1
- Version bump to lxcfs-2.0.6, add README and NEWS to documentation

* Fri Dec 09 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.0.5-3
- Many spec file cleanups/fixes reported by rpmlint

* Fri Dec 09 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.0.5-2
- New package built with tito

* Wed Nov 30 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.0.5-1
- Initial package
