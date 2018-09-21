%{!?lua_version: %global lua_version %{lua: print(string.sub(_VERSION, 5))}}
# for compiled modules
%{!?lua_libdir: %global lua_libdir %{_libdir}/lua/%{lua_version}}
# for arch-independent modules
%{!?lua_pkgdir: %global lua_pkgdir %{_datadir}/lua/%{lua_version}}

Name:       lua-lxc
Version:    3.0.2
Release:    0.1%{?dist}
Summary:    Lua bindings for liblxc

License:    LGPLv2+
URL:        https://linuxcontainers.org/lxc
Source0:    https://linuxcontainers.org/downloads/lxc/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  lua-devel
BuildRequires:  lxc-devel >= 3.0.0
BuildRequires:  make
BuildRequires:  pkgconfig(lua)
Requires:       lua(abi) = %{lua_version}
Requires:       lua-filesystem
Requires:       lxc-libs >= 3.0.0

%description
This package provides Lua bindings for the LXC container API.


%prep
%setup -q


%build
./autogen.sh
%configure
make %{?_smp_mflags}


%install
%make_install


#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license COPYING
# empty:
#doc AUTHORS CONTRIBUTING MAINTAINERS README
%dir %{lua_libdir}/lxc
%{lua_libdir}/lxc/core.so
%{lua_pkgdir}/lxc.lua


%changelog
* Mon May 07 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.0-0.2
- Fix missing dependencies
- Add patch to fix build on CentOS 7

* Wed Apr 18 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.0-0.1
- Initial package
