%global commit          b7ec757d2bea1e5787c3e65b1359b8893491ef90
%global commitdate      20180214
%global shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           python2-lxc
Version:        0.1+git%{commitdate}.%{shortcommit}
Release:        0.2%{?dist}
Summary:        Python 2 bindings for LXC

Group:          Development/Libraries
License:        LGPLv2+
URL:            https://linuxcontainers.org/lxc
Source0:        https://github.com/lxc/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
BuildRequires:  lxc-devel >= 3
BuildRequires:  python2-devel

%{?python_provide:%python_provide python2-lxc}

%description
%{summary}

%prep
%autosetup -n %{name}-%{commit}

%build
%py2_build

%install
%py2_install

%check

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README.md
%{python2_sitearch}/*

%changelog
* Sat Sep 28 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.1+git20180214.b7ec757-0.2
- Rebuild for EPEL-8

* Mon Apr 23 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.1+git20180214.b7ec757-0.1
- Initial package


