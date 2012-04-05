%global modname fabulous

Name:             python-fabulous
Version:          0.1.5
Release:          1%{?dist}
Summary:          Makes your terminal output totally fabulous

Group:            Development/Languages
License:          MIT
URL:              http://pypi.python.org/pypi/fabulous
Source0:          http://lobstertech.com/media/file/fabulous/fabulous-0.1.5.tar.gz

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
%doc

%{python_sitelib}/* 

%changelog
* Thu Apr 05 2012 Ralph Bean <rbean@redhat.com> 0.1.5-1
- initial package for Fedora
