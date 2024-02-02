Name:           tpls-%{tpls_flavor}
Version:        2024
Release:        1%{?dist}
Summary:        [brief description]

License:        [license]
URL:            [URL to project homepage]
Source0:        [URL to source archive]

%if %{tpls_gpu} == "lapack"
Requires:       tpls-%{tpls_flavor}-blas
Requires:       tpls-%{tpls_flavor}-cblas
Requires:       tpls-%{tpls_flavor}-lapack
Requires:       tpls-%{tpls_flavor}-lapacke
Requires:       tpls-%{tpls_flavor}-fspblas
Requires:       tpls-%{tpls_flavor}-scalapack
%endif

Requires:       tpls-%{tpls_flavor}-armadillo
Requires:       tpls-%{tpls_flavor}-blaze
Requires:       tpls-%{tpls_flavor}-cmake
Requires:       tpls-%{tpls_flavor}-exodus
Requires:       tpls-%{tpls_flavor}-hdf5
Requires:       tpls-%{tpls_flavor}-tinyxml2
Requires:       tpls-%{tpls_flavor}-mumps
Requires:       tpls-%{tpls_flavor}-nlopt
Requires:       tpls-%{tpls_flavor}-petsc
Requires:       tpls-%{tpls_flavor}-strumpack
Requires:       tpls-%{tpls_flavor}-suitesparse
Requires:       tpls-%{tpls_flavor}-vtk


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
