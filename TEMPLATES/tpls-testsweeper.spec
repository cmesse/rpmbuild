Name:           tpls-%{tpls_flavor}-testsweeper
Version:        2023.11.05
Release:        1%{?dist}
Summary:        A C++ testing framework for parameter sweeps.

License:        BSD
URL:            https://github.com/icl-utk-edu/testsweeper
Source0:        https://github.com/icl-utk-edu/testsweeper/releases/download/v2023.11.05/testsweeper-%{version}.tar.gz
BuildRequires: make
BuildRequires: tpls-%{tpls_flavor}-cmake

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
%{expand: %setup_tpls_env}

mkdir -p build && cd build
%{tpls_env} \
%{tpls_cmake} .. \
-Dbuild_tests=ON \
%if "%{tpls_libs}" == "static"
-DBUILD_SHARED_LIBS=OFF \
%else
-DBUILD_SHARED_LIBS=ON
%endif

%make_build

%check
cd  build && make test

%install
cd build && %make_install

%files
%{tpls_prefix}/include/testsweeper.hh
%{tpls_prefix}/lib/cmake/testsweeper/testsweeperConfig.cmake
%{tpls_prefix}/lib/cmake/testsweeper/testsweeperConfigVersion.cmake
%{tpls_prefix}/lib/cmake/testsweeper/testsweeperTargets-release.cmake
%{tpls_prefix}/lib/cmake/testsweeper/testsweeperTargets.cmake

%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libtestsweeper.a
%else
%{tpls_prefix}/lib/libtestsweeper.so
%endif

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2023.11.05
- Initial package.

