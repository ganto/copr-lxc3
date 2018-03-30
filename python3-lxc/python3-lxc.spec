Name:           python3-lxc
Version:        3.0.1
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
* Sat Mar 31 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.1-0.1
- Initial package

