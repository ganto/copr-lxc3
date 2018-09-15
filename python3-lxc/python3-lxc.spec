Name:           python3-lxc
Version:        3.0.2
Release:        0.1%{?dist}
Summary:        Python 3 bindings for LXC

Group:          Development/Libraries
License:        LGPLv2+
URL:            https://linuxcontainers.org/lxc
Source0:        https://linuxcontainers.org/downloads/lxc/%{name}-%{version}.tar.gz
BuildRequires:  lxc-devel >= 3
BuildRequires:  pkgconfig(python3) >= 3.2
%if 0%{?rhel} == 7
BuildRequires:  python34-setuptools

# Make sure it will replace python34-lxc < 3.0
Provides:       python34-lxc = %{version}-%{release}
Obsoletes:      python34-lxc < 3.0
Conflicts:      python34-lxc
%endif

%description
%{summary}

%prep
%autosetup -n %{name}-%{version}

%build
%py3_build

%install
%py3_install

%check

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README.md
%{python3_sitearch}/*

%changelog
* Sat Sep 15 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.2-0.1
- Update to 3.0.2

* Wed Jun 20 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.1-0.2
- Fix dependency and upgrade issues on CentOS 7

* Sat Mar 31 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.1-0.1
- Initial package

