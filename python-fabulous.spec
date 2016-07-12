%global modname fabulous

Name:             python-fabulous
Version:          0.3.0
Release:          2%{?dist}
Summary:          Makes your terminal output totally fabulous

Group:            Development/Languages
License:          Apache 2.0 / OFL
URL:              https://jart.github.io/fabulous
Source0:          https://github.com/jart/fabulous/releases/download/0.3.0/fabulous-0.3.0.tar.gz

BuildArch:        noarch

BuildRequires:    gcc
BuildRequires:    python-devel
BuildRequires:    python-setuptools

Requires:         python-imaging

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
* Tue Jul 12 2016 Justine Tunney <jtunney@gmail.com> - 0.3.0-1
- Update for version 0.3.0
- Add Python 3 support

* Mon Jul 7 2016 Justine Tunney <jtunney@gmail.com> - 0.2.1-1
- Update for version 0.2.1

* Mon Jul 4 2016 Justine Tunney <jtunney@gmail.com> - 0.2.0-1
- Update for version 0.2.0
- Change MIT code to Apache 2.0 licence
- Use Google Noto Fonts

* Sun Jul 3 2016 Justine Tunney <jtunney@gmail.com> - 0.1.8-1
- Update for version 0.1.8
- Remove grapefruit dependency

* Fri Apr 20 2012 Ralph Bean <rbean@redhat.com> - 0.1.5-2
- Included README and COPYING in the doc macro

* Thu Apr 05 2012 Ralph Bean <rbean@redhat.com> - 0.1.5-1
- initial package for Fedora
