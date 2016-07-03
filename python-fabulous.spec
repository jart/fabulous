%global modname fabulous

Name:             python-fabulous
Version:          0.1.7
Release:          2%{?dist}
Summary:          Makes your terminal output totally fabulous

Group:            Development/Languages
License:          MIT
URL:              https://jart.github.io/fabulous
Source0:          https://github.com/jart/fabulous/archive/0.1.7.tar.gz

BuildArch:        noarch

BuildRequires:    gcc
BuildRequires:    python-devel
BuildRequires:    python-setuptools

Requires:         python-imaging
Requires:         python-grapefruit

%description
fabulous is a python module for producing fabulously colored terminal output.

Run the demo to see what's available::

    $ python -m fabulous.demo

%prep
%setup -q -n %{modname}-%{version}

%build
%{__python} setup.py build 

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README COPYING

%{python_sitelib}/* 

%changelog
* Fri Apr 20 2012 Ralph Bean <rbean@redhat.com> - 0.1.5-2
- Included README and COPYING in the doc macro

* Thu Apr 05 2012 Ralph Bean <rbean@redhat.com> - 0.1.5-1
- initial package for Fedora
