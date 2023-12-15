Name:           [package-name]
Version:        [version]
Release:        1%{?dist}
Summary:        [brief description]

License:        [license]
URL:            [URL to project homepage]
Source0:        [URL to source archive]

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
