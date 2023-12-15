Name:           [package-name]
Version:        [version]
Release:        1%{?dist}
Summary:        Subroutines to solve sparse linear systems


License:        [license]
URL:            [URL to project homepage]
Source0:        [URL to source archive]

BuildRequires:  [build dependencies]
Requires:       [runtime dependencies]

%description
SuperLU contains a set of subroutines to solve a sparse linear system
A*X=B. It uses Gaussian elimination with partial pivoting (GEPP).
The columns of A may be preordered before factorization; the
preordering for sparsity is completely separate from the factorization.



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
