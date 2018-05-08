%if 0%{?fedora}
%global with_devel 1
%global with_bundled 1
%global with_debug 1
%global with_check 1
%global with_unit_test 1
%else
%global with_devel 1
%global with_bundled 1
%global with_debug 1
%global with_check 1
%global with_unit_test 1
%endif

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**}; 
%endif

%global provider        github
%global provider_tld    com
%global project         lxc
%global repo            distrobuilder
# https://github.com/lxc/distrobuilder
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          406fd5fe7dec4a969ec08bdf799c8ae483d37489
%global commitdate      20180428
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:       %{repo}
Version:    0
Release:    0.1.%{commitdate}git%{shortcommit}%{?dist}
Summary:    System container image builder for LXC and LXD

License:    ASL 2.0
URL:        https://%{provider_prefix}
Source0:    https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source1:    distrobuilder-dist-20180508.tar.gz
Patch0:     distrobuilder-5c6ad30-Disable-online-tests.patch

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%if ! 0%{?with_bundled}
BuildRequires:  golang(github.com/lxc/lxd/shared)
BuildRequires:  golang(github.com/lxc/lxd/shared/api)
BuildRequires:  golang(github.com/lxc/lxd/shared/ioprogress)
BuildRequires:  golang(github.com/lxc/lxd/shared/osarch)
BuildRequires:  golang(github.com/spf13/cobra)
BuildRequires:  golang(gopkg.in/flosch/pongo2.v3)
BuildRequires:  golang(gopkg.in/yaml.v2)
%endif

Requires:       gnupg
Requires:       squashfs-tools
Requires:       tar

%description
%{summary}.

%if 0%{?with_devel}
%package devel
Summary:        System container image builder - Source Libraries
BuildArch:      noarch

%if 0%{?with_check}
BuildRequires:  gnupg
BuildRequires:  squashfs-tools

%if ! 0%{?with_bundled}
BuildRequires:  golang(github.com/lxc/lxd/shared)
BuildRequires:  golang(github.com/lxc/lxd/shared/api)
BuildRequires:  golang(github.com/lxc/lxd/shared/ioprogress)
BuildRequires:  golang(github.com/lxc/lxd/shared/osarch)
BuildRequires:  golang(github.com/spf13/cobra)
BuildRequires:  golang(gopkg.in/flosch/pongo2.v3)
BuildRequires:  golang(gopkg.in/yaml.v2)
%endif
%endif

%if ! 0%{?with_bundled}
Requires:       golang(github.com/lxc/lxd/shared)
Requires:       golang(github.com/lxc/lxd/shared/api)
Requires:       golang(github.com/lxc/lxd/shared/ioprogress)
Requires:       golang(github.com/lxc/lxd/shared/osarch)
Requires:       golang(github.com/spf13/cobra)
Requires:       golang(gopkg.in/flosch/pongo2.v3)
Requires:       golang(gopkg.in/yaml.v2)
%endif

Provides:       golang(%{import_path}/generators) = %{version}-%{release}
Provides:       golang(%{import_path}/image) = %{version}-%{release}
Provides:       golang(%{import_path}/managers) = %{version}-%{release}
Provides:       golang(%{import_path}/shared) = %{version}-%{release}
Provides:       golang(%{import_path}/sources) = %{version}-%{release}

%description devel
%{summary}.

This package contains library sources intended for building other packages
which use the import path %{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary:        Unit tests for %{name} package
BuildArch:      noarch
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

# test subpackage tests code from devel subpackage
Requires:       %{name}-devel = %{version}-%{release}

%if ! 0%{?with_bundled}
Requires:       golang(github.com/lxc/lxd/shared)
Requires:       golang(gopkg.in/flosch/pongo2.v3)
%endif
Requires:       gnupg
Requires:       squashfs-tools

%description unit-test-devel
%{summary}.

This package contains unit tests for project providing packages with
%{import_path} prefix.
%endif

%prep
%autosetup -n %{repo}-%{commit} -p1
tar zxf %{SOURCE1}

%if 0%{?with_bundled}
# move content of vendor under Godeps as has been so far
mkdir -p Godeps/_workspace/src
mv dist/src/* Godeps/_workspace/src/.
%endif

%build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../ src/%{import_path}

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
export GOPATH=$(pwd):$(pwd)/Godeps/_workspace:%{gopath}
%endif

%gobuild -o _bin/%{name} %{import_path}/%{name}

%install
install -d %{buildroot}%{_bindir}
install -p -m 755 _bin/%{name} %{buildroot}%{_bindir}/%{name}

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test.file-list
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
export GOPATH=%{buildroot}/%{gopath}:$(pwd)/Godeps/_workspace:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}/image
%gotest %{import_path}/generators
%gotest %{import_path}/shared

%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license COPYING
%doc *.md
%doc doc/examples
%{_bindir}/%{name}

%if 0%{?with_devel}
%files devel -f devel.file-list
%license COPYING
%doc *.md
%endif

%if 0%{?with_unit_test}
%files unit-test-devel -f unit-test.file-list
%license COPYING
%doc *.md
%endif

%changelog
* Tue May 08 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0-0.1.20180428git406fd5f
- Update to commit 406fd5f from Apr 28, 2018

* Wed Apr 04 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0-0.1.20180403gitc0e1763
- Initial package

