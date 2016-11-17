%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name simplecov-html

Summary:       Default HTML formatter for SimpleCov
Name:          %{?scl_prefix}rubygem-%{gem_name}
Version:       0.10.0
Release:       5%{?dist}
Group:         Development/Languages
License:       MIT
URL:           https://github.com/colszowka/simplecov-html
Source0:       http://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires:      %{?scl_prefix_ruby}ruby(release)
Requires:      %{?scl_prefix_ruby}ruby
Requires:      %{?scl_prefix_ruby}rubygems
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}rubygem(test-unit)
BuildRequires: %{?scl_prefix}rubygem(simplecov)
BuildArch:     noarch
Provides:      %{?scl_prefix}rubygem(%{gem_name}) = %{version}

# Explicitly require runtime subpackage, as long as older scl-utils do not generate it
Requires: %{?scl_prefix}runtime

%description
Default HTML formatter for SimpleCov code coverage tool for ruby 1.9+

%package doc
Summary:   Documentation for %{pkg_name}
Group:     Documentation
Requires:  %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

#cleanup
rm -f %{buildroot}%{gem_instdir}/.document
rm -f %{buildroot}%{gem_instdir}/.gitignore
rm -f %{buildroot}%{gem_instdir}/.rubocop.yml
rm -f %{buildroot}%{gem_instdir}/.travis.yml
rm -f %{buildroot}%{gem_instdir}/.yardopts
rm -rf %{buildroot}%{gem_instdir}/.yardoc
rm -f %{buildroot}%{gem_instdir}/Gemfile
rm -f %{buildroot}%{gem_instdir}/simplecov-html.gemspec

%check
pushd .%{gem_instdir}
# Remove bundler require
sed -i '/bundler/ s/^/#/' test/helper.rb

%{?scl:scl enable %{scl} - << \EOF}
ruby -I.:lib:test -e "Dir.glob('./test/test_*.rb').each {|t| require t}"
%{?scl:EOF}
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%{gem_instdir}/assets
%{gem_instdir}/public
%{gem_instdir}/views
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Guardfile
%{gem_instdir}/Rakefile
%{gem_instdir}/README.md
%{gem_instdir}/test

%changelog
* Fri Apr 08 2016 Pavel Valena <pvalena@redhat.com> - 0.10.0-5
- Fix tests execution

* Fri Apr 08 2016 Pavel Valena <pvalena@redhat.com> - 0.10.0-4
- Enable tests

* Wed Apr 06 2016 Pavel Valena <pvalena@redhat.com> - 0.10.0-3
- Add scl macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 21 2015 Troy Dawson <tdawson@redhat.com> - 0.10.0-1
- Updated to version 0.10.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Troy Dawson <tdawson@redhat.com> - 0.8.0-2
- fix for correct EPEL7 build

* Tue Feb 04 2014 Troy Dawson <tdawson@redhat.com> - 0.8.0-1
- Updated to version 0.8.0
- Update to latest ruby spec guidelines

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Troy Dawson <tdawson@redhat.com> - 0.7.1-3
- Fix to make it build/install on F19+

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Troy Dawson <tdawson@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Mon Aug 27 2012 Troy Dawson <tdawson@redhat.com> - 0.5.3-1
- Initial package
