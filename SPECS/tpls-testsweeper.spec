Name:           tpls-%{tpls_flavor}-testsweeper
Version:        2023.11.05
Release:        1%{?dist}
Summary:        A C++ testing framework for parameter sweeps.

License:        BSD
URL:            https://github.com/icl-utk-edu/testsweeper
Source0:        https://github.com/icl-utk-edu/testsweeper/archive/refs/tags/testsweeper-%{version}.tar.gz

BuildRequires: make
BuildRequires: cmake

BuildRequires:      %{tpls_rpm_cc}  >= %{tpls_comp_minver}
BuildRequires:      %{tpls_rpm_cxx} >= %{tpls_comp_minver}

%description
TestSweeper is a C++ testing framework for parameter sweeps.
It handles parsing command line options, iterating over the test space,
and printing results. This simplifies test functions by allowing them to
concentrate on setting up and solving one problem at a time.

TestSweeper is part of the SLATE project
(Software for Linear Algebra Targeting Exascale), which is funded by
the Department of Energy as part of its Exascale Computing Initiative
(ECP).

%prep
%setup -q -n testsweeper-%{version}

%build

%if "%{tpls_compiler}" == "intel"
if [ "$SETVARS_COMPLETED" != "1" ]; then
	source /opt/intel/oneapi/setvars.sh intel64
fi
%endif

mkdir -p build && cd build && LDFLAGS="%{tpls_ldflags} %{tpls_rpath}" %{tpls_compilers} LD=%{tpls_cxx} cmake \
-DCMAKE_INSTALL_PREFIX=%{tpls_prefix} \
-DCMAKE_CXX_COMPILER=%{tpls_cxx} \
-DCMAKE_INSTALL_LIBDIR=%{tpls_libdir} \
%if %{tpls_check} == 1
-Dbuild_tests=ON \
%endif
%if "%{tpls_libs}" == "static"
-DBUILD_SHARED_LIBS=OFF \
%else
-DCMAKE_CXX_FLAGS=-fPIC \
-DBUILD_SHARED_LIBS=ON \
%endif
..

%make_build

%check
make check

%install
cd build && %make_install

%files
%{tpls_prefix}/include/testsweeper.hh
%{tpls_prefix}/%{tpls_libdir}/cmake/testsweeper/testsweeperConfig.cmake
%{tpls_prefix}/%{tpls_libdir}/cmake/testsweeper/testsweeperConfigVersion.cmake
%{tpls_prefix}/%{tpls_libdir}/cmake/testsweeper/testsweeperTargets-noconfig.cmake
%{tpls_prefix}/%{tpls_libdir}/cmake/testsweeper/testsweeperTargets.cmake
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/%{tpls_libdir}/libtestsweeper.a
%else
%{tpls_prefix}/%{tpls_libdir}/libtestsweeper.so
%endif

%changelog
* Tue Dec 12 2023 Christian Messe <cmesse@lbl.gov> - 2023.11.05
- Initial package.

