%global gem_name ruby-lxc

Name:       rubygem-%{gem_name}
Version:    1.2.3
Release:    0.1%{?dist}
Summary:    Ruby bindings for liblxc
License:    LGPLv2+
URL:        https://github.com/lxc/ruby-lxc
Source0:    https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1:    README.md

BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
# Compiler is required for build of gem binary extension.
# https://fedoraproject.org/wiki/Packaging:C_and_C++#BuildRequires_and_Requires
BuildRequires: gcc
BuildRequires: lxc-devel

%description
Ruby-LXC is a Ruby binding for the liblxc library, allowing
Ruby scripts to create and manage Linux containers.


%package doc
Summary:    Documentation for %{name}
Requires:   %{name} = %{version}-%{release}
BuildArch:  noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}
gem spec %{SOURCE0} -l --ruby > %{gem_name}-%{version}.gemspec

%setup -q -D -T -n  %{gem_name}-%{version}

%build
# Create the gem as gem install only works on a gem file
gem build ../%{gem_name}-%{version}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
%if 0%{?rhel} == 7
mkdir -p %{buildroot}%{gem_extdir_mri}/lib/lxc
mv %{buildroot}%{gem_dir}/gems/%{gem_name}-%{version}/lib/lxc/lxc.so %{buildroot}%{gem_extdir_mri}/lib/lxc/
%else
cp -a ./%{gem_extdir_mri}/lxc %{buildroot}%{gem_extdir_mri}/
%endif

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/

cp %{SOURCE1} .


%check
pushd .%{gem_instdir}
# Run the test suite.
popd

%files
%doc README.md
%dir %{gem_instdir}
%{gem_extdir_mri}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}


%changelog
* Fri Jun 08 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.2.2-0.1
- Initial package
