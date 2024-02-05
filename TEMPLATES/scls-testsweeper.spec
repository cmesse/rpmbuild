%define scls_oflags -O2

Name:           scls-%{scls_flavor}-testsweeper
Version:        2023.11.05
Release:        1%{?dist}
Summary:        A C++ testing framework for parameter sweeps

License:        BSD
URL:            https://github.com/icl-utk-edu/testsweeper
Source0:        https://github.com/icl-utk-edu/testsweeper/releases/download/v2023.11.05/testsweeper-%{version}.tar.gz
BuildRequires:  make
BuildRequires:  scls-%{scls_flavor}-cmake

BuildRequires:      %{scls_rpm_cc}  >= %{scls_comp_minver}
BuildRequires:      %{scls_rpm_cxx} >= %{scls_comp_minver}

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
%{expand: %setup_scls_env}

mkdir -p build && cd build
%{scls_env} \
%{scls_cmake} \
    -DCMAKE_CXX_COMPILER=%{scls_cxx} \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags}" \
    -Dbuild_tests=ON \
%if "%{scls_libs}" == "static"
    -DBUILD_SHARED_LIBS=OFF \
%else
    -DBUILD_SHARED_LIBS=ON \
%endif
    ..

%make_build

%check
cd build && make test

%install
cd build
%make_install

%files
%{scls_prefix}/include/testsweeper.hh
%{scls_prefix}/lib/cmake/testsweeper/testsweeperConfig.cmake
%{scls_prefix}/lib/cmake/testsweeper/testsweeperConfigVersion.cmake
%{scls_prefix}/lib/cmake/testsweeper/testsweeperTargets-release.cmake
%{scls_prefix}/lib/cmake/testsweeper/testsweeperTargets.cmake

%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libtestsweeper.a
%else
%{scls_prefix}/lib/libtestsweeper.so
%endif

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2023.11.05
- Initial package.

