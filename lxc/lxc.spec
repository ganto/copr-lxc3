%if 0%{?fedora}
%global with_seccomp 1
%endif

%if 0%{?rhel} >= 7
%ifarch %{ix86} x86_64 %{arm} aarch64
%global with_seccomp 1
%endif
%endif

Name:           lxc
Version:        3.1.0
Release:        0.1%{?dist}
Summary:        Linux Resource Containers
License:        LGPLv2+ and GPLv2
URL:            http://linuxcontainers.org
Source0:        http://linuxcontainers.org/downloads/%{name}-%{version}.tar.gz
Patch0:         lxc-2.0.6-fix-lxc-net.patch
BuildRequires:  docbook2X
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  kernel-headers
BuildRequires:  libselinux-devel
%if 0%{?with_seccomp}
BuildRequires:  pkgconfig(libseccomp)
%endif # with_seccomp
BuildRequires:  libcap-devel
BuildRequires:  libtool
BuildRequires:  pam-devel
BuildRequires:  systemd
%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:  pkgconfig(bash-completion)
%endif
# lxc-extra subpackage not needed anymore, lxc-ls has been rewriten in
# C and does not depend on the Python3 binding anymore
Provides:       lxc-extra = %{version}-%{release}
Obsoletes:      lxc-extra < 1.1.5-3

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%description
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.


%package           libs
Summary:           Runtime library files for %{name}
# rsync is called in bdev.c, e.g. by lxc-clone
Requires:          rsync
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd
Requires(post):    /sbin/ldconfig
Requires(postun):  /sbin/ldconfig
# used by download template
Requires:          gnupg
Requires:          wget
%if 0%{?fedora}
Recommends:        dnsmasq
Recommends:        iptables
%endif


%description    libs
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The %{name}-libs package contains libraries for running %{name} applications.

%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}core\\.so\\.0


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description    doc
This package contains documentation for %{name}.


%package -n     pam_cgfs                     
Summary:        CGroup file system PAM module
                                                                               
%description -n pam_cgfs                                            
When a user logs in, this pam module will create cgroups which the user
may administer, either for all controllers or for any controllers listed
on the command line. 


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
%configure --enable-capabilities \
           --enable-doc \
           --enable-api-docs \
           --disable-silent-rules \
           --docdir=%{_pkgdocdir} \
           --disable-rpath \
           --disable-static \
           --disable-apparmor \
           --enable-pam \
           --enable-selinux \
%if 0%{?with_seccomp}
           --enable-seccomp \
%endif # with_seccomp
           --with-init-script=systemd \
           --disable-werror \
# intentionally blank line

# fix rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%{make_build} %{?_smp_mflags}


%install
%{make_install} %{?_smp_mflags}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

# docs
mkdir -p %{buildroot}%{_pkgdocdir}
cp -a AUTHORS README %{!?_licensedir:COPYING} %{buildroot}%{_pkgdocdir}
mkdir -p %{buildroot}%{_pkgdocdir}/api
cp -a doc/api/html/* %{buildroot}%{_pkgdocdir}/api/

# cache dir
mkdir -p %{buildroot}%{_localstatedir}/cache/%{name}

# remove libtool .la file
rm -rf %{buildroot}%{_libdir}/liblxc.la


%check
make check


%post libs
/sbin/ldconfig
%systemd_post %{name}-net.service
%systemd_post %{name}.service
%systemd_post %{name}@.service


%preun libs
%systemd_preun %{name}-net.service
%systemd_preun %{name}.service
%systemd_preun %{name}@.service


%postun libs
/sbin/ldconfig
%systemd_postun %{name}-net.service
%systemd_postun %{name}.service
%systemd_postun %{name}@.service


%files
%{_bindir}/%{name}-*
%{_mandir}/man1/%{name}*
%{_mandir}/*/man1/%{name}*
# in lxc-libs:
%exclude %{_bindir}/%{name}-autostart
%exclude %{_mandir}/man1/%{name}-autostart*
%exclude %{_mandir}/*/man1/%{name}-autostart*
%exclude %{_mandir}/man1/%{name}-user-nic*
%exclude %{_mandir}/*/man1/%{name}-user-nic*
%{_datadir}/%{name}/%{name}.functions
%if 0%{?fedora} || 0%{?rhel} >= 7
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/%{name}
%else
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/%{name}
%endif


%files libs
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/templates
%dir %{_datadir}/%{name}/config
%{_datadir}/%{name}/config/*
%{_datadir}/%{name}/hooks
%{_datadir}/%{name}/%{name}-patch.py*
%{_datadir}/%{name}/selinux
%{_datadir}/%{name}/templates/lxc-*
%{_libdir}/liblxc.so.*
%{_libdir}/%{name}
%{_libexecdir}/%{name}
# fixme: should be in libexecdir?
%{_sbindir}/init.%{name}
%{_bindir}/%{name}-autostart
%{_sharedstatedir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/default.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_mandir}/man1/%{name}-autostart*
%{_mandir}/*/man1/%{name}-autostart*
%{_mandir}/man1/%{name}-user-nic*
%{_mandir}/*/man1/%{name}-user-nic*
%{_mandir}/man5/%{name}*
%{_mandir}/man7/%{name}*
%{_mandir}/*/man5/%{name}*
%{_mandir}/*/man7/%{name}*
%dir %{_pkgdocdir}
%{_pkgdocdir}/AUTHORS
%if 0%{?_licensedir:1}
%license COPYING
%else
%{_pkgdocdir}/COPYING
%endif
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}@.service
%{_unitdir}/%{name}-net.service
%dir %{_localstatedir}/cache/%{name}


%files devel
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/lxc
%{_libdir}/liblxc.so


%files doc
%dir %{_pkgdocdir}
# README, AUTHORS and COPYING intentionally duplicated because -doc
# can be installed on its own.
%{_pkgdocdir}/*
%if 0%{?_licensedir:1}
%license COPYING
%endif


%files -n pam_cgfs                                                                  
%doc AUTHORS                                                                        
%license COPYING                                                                    
%defattr(-,root,root)                                                               
/%{_lib}/security/pam_cgfs.so


%changelog
* Wed Nov 28 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.3-0.1
- Update to 3.0.3

* Sat Sep 15 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.2-0.2
- Add patch to fix build error on CentOS 7
- Cleanup unused Lua build dependency

* Sat Sep 15 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.2-0.1
- Update to 3.0.2

* Wed Jun 06 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.1-0.1
- Update to 3.0.1

* Sat Mar 31 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.0-0.1
- Update to 3.0.0

* Wed Oct 25 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.1.1-0.1
- Update to 2.1.1.

* Wed Sep 27 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.1.0-0.1
- Update to 2.1.0.
- Add setuptools dependency for EPEL 7 builds

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 10 2017 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.8-2
- Fix for EL6 build failure.
- Fix bash completion on epel6 (rhbz#1408173).

* Tue Jun  6 2017 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.8-1
- Update to 2.0.8.

* Thu Mar  9 2017 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.7-2
- Add fix for CVE-2017-5985.

* Wed Feb 15 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.0.7-1.2
- Rebuild for brp-python-bytecompile

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 29 2017 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.7-1
- Update to 2.0.7.

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.0.6-2.1
- Rebuild for Python 3.6

* Sun Dec  4 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.6-2
- Enable python3 on epel7 builds.
- Fix dependency on network-online.target for lxc-net.service.

* Sat Dec  3 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.6-1
- Update to 2.0.6.

* Wed Oct  5 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.5-1
- Update to 2.0.5.

* Tue Aug 16 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.4-1
- Update to 2.0.4.
- Remove conditional for eol'ed Fedora releases.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-1.1
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 29 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.3-1
- Update to 2.0.3.
- Merge spec file cleanups by Thierry Vignaud (tvignaud@redhat.com).

* Fri Jun  3 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.1-1
- Update to 2.0.1.
- Remove patch no longer needed.

* Wed Apr 20 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.0-1
- Update to 2.0.0.
- Obsolete the -extra subpackage.
- Move the completion file to %%{_datadir}.

* Tue Mar  1 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.5-2
- Power64 and s390(x) now have libseccomp support

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 15 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.5-1
- Update to 1.1.5.
- Update patch.

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2.1
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 21 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.4-2
- Add patch to fix bootorder (rhbz#1263612).

* Sat Oct 17 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.4-1
- Update to 1.1.4.

* Thu Oct  1 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.3-2
- Add security fix, see rhbz#1267844.

* Sat Aug 15 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.3-1
- Update to 1.1.3.
- Remove patches applied upstream.

* Sun Aug  2 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.2-2
- Add security fixes, see rhbz#1245939 and rhbz#1245941.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 20 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.2-1
- Update to 1.1.2.
- Add patch to fix building of the lua bindings.

* Tue Mar 17 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.1-2
- Use %%license only where possible.

* Tue Mar 17 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.1-1
- Update to 1.1.1.
- Add dependency on rsync (rhbz#1177981).
- Tag COPYING with %%licence.

* Mon Feb 16 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.0-3
- aarch64 now has seccomp support

* Tue Feb 10 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.0-2
- lxc-top no longer relies on the lua bindings.
- lxc-device no longer relies on the python3 bindings.
- Spec file cleanups.

* Sun Feb  8 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.0-1
- Update to 1.1.0.

* Sat Aug 30 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.0-0.3.alpha1
- Add missing dependency on lua-alt-getopt (rhbz#1131707).

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.2.alpha1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 11 2014 Jakub Čajka <jcajka@redhat.com> - 1.1.0-0.2.alpha1
- Fixed build dependencies on s390(x) and ppc(64(le))

* Sun Aug 10 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.0-0.1.alpha1
- Update to 1.1.0.alpha1.

* Fri Aug  8 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.5-2
- Include sysvinit resp. systemd support for autostart of containers.
- Do not list explicit requirements for templates.
- Add missing dependency on lxc-lua for lxc-top.
- Include apidocs.

* Fri Aug  8 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.5-1
- Update to 1.0.5

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun  4 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.3-1
- Update to 1.0.3.
- Remove obsolete patches.
- Add systemd support.
- Lua bindings are not optional (needed e.g. for lxc-top).

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Jan 30 2014 Marek Goldmann <mgoldman@redhat.com> - 0.9.0-3
- There is still no Python 3 available in EPEL 7

* Wed Sep  4 2013 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.0-2
- Small fix to the included Fedora template.

* Sun Sep  1 2013 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.0-1
- Update to 0.9.0.
- Make the -libs subpackage installable on its own:
  - Move files needed by the libraries to the subpackage.
  - Let packages depend on -libs.
- Add rsync as dependency to the templates package.
- Add (optional) subpackages for Python3 and Lua bindings.
- Add upstream patches for the Fedora template.
- Define and use the _pkgdocdir macro, also fixing rhbz#1001235.
- Update License tag.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar  2 2013 Thomas Moschny <thomas.moschny@gmx.de> - 0.8.0-2
- Add upstream patch fixing the release url in the Fedora template.

* Fri Feb 15 2013 Thomas Moschny <thomas.moschny@gmx.de> - 0.8.0-1
- Update to 0.8.0.
- Modernize spec file.
- Include more templates.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 26 2012 Thomas Moschny <thomas.moschny@gmx.de> - 0.7.5-1
- Update to upstream 0.7.5
- No need to run autogen.sh
- Fix: kernel header asm/unistd.h was not found
- Specfile cleanups

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 06 2011 Adam Miller <maxamillion@fedoraproject.org> - 0.7.4.2-1
- Update to upstream 0.7.4.2

* Fri Mar 25 2011 Silas Sewell <silas@sewell.ch> - 0.7.4.1-1
- Update to 0.7.4.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 26 2010 Silas Sewell <silas@sewell.ch> - 0.7.2-1
- Update to 0.7.2
- Remove templates

* Tue Jul 06 2010 Silas Sewell <silas@sewell.ch> - 0.7.1-1
- Update to 0.7.1

* Wed Feb 17 2010 Silas Sewell <silas@sewell.ch> - 0.6.5-1
- Update to latest release
- Add /var/lib/lxc directory
- Patch for sys/stat.h

* Fri Nov 27 2009 Silas Sewell <silas@sewell.ch> - 0.6.4-1
- Update to latest release
- Add documentation sub-package

* Mon Jul 27 2009 Silas Sewell <silas@sewell.ch> - 0.6.3-2
- Apply patch for rawhide kernel

* Sat Jul 25 2009 Silas Sewell <silas@sewell.ch> - 0.6.3-1
- Initial package
