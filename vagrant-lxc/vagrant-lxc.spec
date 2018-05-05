%global vagrant_plugin_name vagrant-lxc

Name: %{vagrant_plugin_name}
Version: 1.4.1
Release: 0.2%{?dist}
Summary: LXC provider for vagrant
Group: Development/Languages
License: MIT
URL: https://github.com/fgrehm/vagrant-lxc
Source0: https://rubygems.org/gems/%{vagrant_plugin_name}-%{version}.gem

# script needed to generate the vagrant-lxc sudo wrapper script from template.
# part of this srpm
Source1: create_wrapper.rb

Patch1: vagrant-1.4.1-Fix-sudo-wrapper-for-use-in-system-wide-plugin.patch

Requires(pre): shadow-utils
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: lxc
Requires: lxc-extra
Requires: vagrant >= 1.9.1

BuildRequires: vagrant >= 1.9.1
BuildRequires: rubygem(rdoc)
BuildRequires: rubygem(rspec)
BuildArch: noarch

%description
LXC provider for vagrant.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{vagrant_plugin_name}-%{version}

%patch1 -p1

gem spec %{SOURCE0} -l --ruby > %{vagrant_plugin_name}.gemspec


%build
gem build %{vagrant_plugin_name}.gemspec
%vagrant_plugin_install

%install
mkdir -p %{buildroot}%{vagrant_plugin_dir}
cp -a .%{vagrant_plugin_dir}/* \
        %{buildroot}%{vagrant_plugin_dir}/

ruby -I %{vagrant_dir}/lib %{SOURCE1} %{buildroot}%{vagrant_plugin_instdir}/templates
install -m 0555 ./vagrant-lxc-wrapper %{buildroot}%{vagrant_plugin_instdir}/scripts/vagrant-lxc-wrapper

echo "%vagrant ALL=(root) NOPASSWD: %{vagrant_plugin_instdir}/scripts/vagrant-lxc-wrapper" > ./sudoers_file
mkdir -p %{buildroot}%{_sysconfdir}/sudoers.d
install -m 0440 ./sudoers_file %{buildroot}%{_sysconfdir}/sudoers.d/vagrant-lxc

%check
pushd .%{vagrant_plugin_instdir}
sed -i '/bundler/ s/^/#/' spec/spec_helper.rb

rspec -I%{vagrant_dir}/lib spec
popd

%pre
getent group vagrant >/dev/null || groupadd -r vagrant

%files
%dir %{vagrant_plugin_instdir}
%license %{vagrant_plugin_instdir}/LICENSE.txt
%doc %{vagrant_plugin_instdir}/README.md
%{vagrant_plugin_libdir}
%{vagrant_plugin_instdir}/locales
%exclude %{vagrant_plugin_cache}
%exclude %{vagrant_plugin_instdir}/.gitignore
%{vagrant_plugin_spec}
%attr(440, root, root) %{_sysconfdir}/sudoers.d/vagrant-lxc

%exclude %{vagrant_plugin_instdir}/.rspec
%exclude %{vagrant_plugin_instdir}/.travis.yml
%exclude %{vagrant_plugin_instdir}/.vimrc
%dir %{vagrant_plugin_instdir}/scripts
%{vagrant_plugin_instdir}/scripts/lxc-template
%{vagrant_plugin_instdir}/scripts/pipework
%attr(755, root, root) %{vagrant_plugin_instdir}/scripts/vagrant-lxc-wrapper
%dir %{vagrant_plugin_instdir}/templates
%{vagrant_plugin_instdir}/templates/sudoers.rb.erb


%files doc
%doc %{vagrant_plugin_docdir}
%doc %{vagrant_plugin_instdir}/CHANGELOG.md
%doc %{vagrant_plugin_instdir}/BOXES.md
%doc %{vagrant_plugin_instdir}/CONTRIBUTING.md
%{vagrant_plugin_instdir}/Rakefile
%{vagrant_plugin_instdir}/Gemfile
%{vagrant_plugin_instdir}/vagrant-lxc.gemspec
%{vagrant_plugin_instdir}/spec
%exclude %{vagrant_plugin_instdir}/spec/support/.gitkeep
%{vagrant_plugin_instdir}/Guardfile
%dir %{vagrant_plugin_instdir}/tasks
%{vagrant_plugin_instdir}/tasks/spec.rake
%{vagrant_plugin_instdir}/vagrant-spec.config.rb

%changelog
* Sat May 05 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.4.1-0.2
- Update patch for vagrant-lxc-wrapper fixes

* Fri May 04 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.4.1-0.1
- Update to 1.4.1.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 14 2017 Vít Ondruch <vondruch@redhat.com> - 1.1.0-11
- Drop registration plugins for Vagrant 1.9.1 compatibility.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 18 2015 Michael Adam <madam@redhat.com> - 1.1.0-7
- Add missing dependency for lxc-extra (BZ #1193438).

* Thu Jan 29 2015 Michael Adam <madam@redhat.com> - 1.1.0-6
- Make some non-standard perms explicit in the files section.
- Own directories that we create.

* Tue Jan 27 2015 Michael Adam <madam@redhat.com> - 1.1.0-5
- Cleanup specfile.

* Mon Jan 26 2015 Michael Adam <madam@redhat.com> - 1.1.0-4
- Ship precreated sudo-wrapper and sudoers file.

* Mon Jan 26 2015 Michael Adam <madam@redhat.com> - 1.1.0-3
- Capitalize summary and description.
- Fix sudo wrapper and "vagrant lxc sudoers" mechansim from upstream.

* Mon Jan 26 2015 Michael Adam <madam@redhat.com> - 1.1.0-2
- Move some files from -doc to main package.

* Sat Jan 24 2015 Michael Adam <madam@redhat.com> - 1.1.0-1
- Initial package for Fedora
