Name:		  lxcfs
Version:	  3.0.1
Release:	  0.1%{?dist}
Summary:	  FUSE based filesystem for LXC
License:	  ASL 2.0
URL:		  https://linuxcontainers.org/lxcfs
Source0:	  https://linuxcontainers.org/downloads/%{name}/%{name}-%{version}.tar.gz
BuildRequires:	  gcc
BuildRequires:	  gawk
BuildRequires:	  make
BuildRequires:	  fuse-devel
BuildRequires:	  help2man
BuildRequires:	  systemd
Requires(post):	  systemd
Requires(preun):  systemd
Requires(postun): systemd
# for /usr/share/lxc/config/common.conf.d:
Requires:	  lxc-templates


%description
LXCFS is a simple userspace filesystem designed to work around some
current limitations of the Linux kernel.

Specifically, it's providing two main things

- A set of files which can be bind-mounted over their /proc originals
  to provide CGroup-aware values.

- A cgroupfs-like tree which is container aware.

The code is pretty simple, written in C using libfuse.

The main driver for this work was the need to run systemd based
containers as a regular unprivileged user while still allowing systemd
inside the container to interact with cgroups.

Now with the introduction of the cgroup namespace in the Linux kernel,
that part is no longer necessary on recent kernels and focus is now on
making containers feel more like a real independent system through the
proc masking feature.


%prep
%autosetup


%build
# configure on CentOS still defaults to sysvinit
%configure --with-init-script=systemd
make %{?_smp_mflags}


%install
%make_install SYSTEMD_UNIT_DIR=%{_unitdir}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}


%post
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun %{name}.service


%files
%doc AUTHORS
# empty:
#doc ChangeLog NEWS README
%license COPYING
%{_bindir}/lxcfs
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/lib%{name}.so
%exclude %{_libdir}/%{name}/lib%{name}.la
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/lxc.mount.hook
%{_datadir}/%{name}/lxc.reboot.hook
%{_mandir}/man1/%{name}.1*
%{_unitdir}/%{name}.service
%{_datadir}/lxc/config/common.conf.d/00-lxcfs.conf
%dir %{_sharedstatedir}/%{name}


%changelog
* Tue Apr 17 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.0-0.3
- Always enforce systemd init, fixes build failure on CentOS

* Mon Apr 16 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.0-0.2
- Adjust to "official" lxcfs-3.0.0-1 by thm in updates-testing

* Sat Mar 31 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.0-0.1
- Update to 3.0.0

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
