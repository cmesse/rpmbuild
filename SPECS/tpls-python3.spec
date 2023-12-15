
%global pybasever 3.12

Name:           tpls-%{tpls_flavor}-python
Version:        3.12.1
Release:        1%{?dist}
Summary: Version %{pybasever} of the Python interpreter

License: Python
URL:            [URL to project homepage]
Source0:        https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz

BuildRequires:  [build dependencies]
Requires:       [runtime dependencies]

%description
[Longer, detailed description of the package]

%prep
%setup -q

%build
[build commands, e.g., ./configure, make]

%install
[install commands, e.g., make install DESTDIR=%{buildroot}]

%files
[files to include in the package, e.g., /usr/bin/myapp]

%changelog
* [date] [packager] - [version]-1
- Initial package.
