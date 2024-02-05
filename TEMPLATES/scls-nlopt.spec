%define scls_oflags -O2

Name:           scls-%{scls_flavor}-nlopt
Version:        2.7.1
Release:        1%{?dist}
Summary:        nonlinear local and global optimization

# The detailed license-breakdown of the sources is:
#
# BSD (2 clause)
# --------------
# util/mt19937ar.c
#
#
# BSD (3 clause)
# --------------
# slsqp/*
#
#
# LGPL (v2 or later)
# ------------------
# luksan/*
#
# MIT/X11 (BSD like)
# ------------------
# api/*    auglag/*  bobyqa/*      cdirect/*  cobyla/*
# cquad/*  crs/*     direct/*      esch/*     isres/*
# mlsl/*   mma/*     neldermead/*  newuoa/*   octave/*
# stogo/*  tensor/*  test/*        util/* (ex. util/mt19937ar.c)
#
#
# Public Domain
# -------------
# praxis/*  subplex/*
#
License:        BSD and LGPLv2+ and MIT and Public Domain
URL:            https://nlopt.readthedocs.io/
Source0:        https://github.com/stevengj/nlopt/archive/v%{version}.tar.gz

BuildRequires:  scls-%{scls_flavor}-cmake
BuildRequires:  ncurses-devel

%if "%{scls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%else
BuildRequires:  scls-%{scls_flavor}-%{scls_mpi}
Requires:       scls-%{scls_flavor}-%{scls_mpi}
%endif

%description
NLopt is a library for nonlinear local and global optimization, for
functions with and without gradient information.  It is designed as
as simple, unified interface and packaging of several free/open-source
nonlinear optimization libraries.

It features bindings for GNU Guile, Octave and Python.  This build has
been made with C++-support enabled.

%prep
%setup -q -n nlopt-%{version}

%build
%{expand: %setup_scls_env}

mkdir build && cd build
%{scls_env} \
%{scls_cmake} \
	-DCMAKE_C_COMPILER=%{scls_mpicc} \
    -DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags}" \
    -DCMAKE_CXX_COMPILER=%{scls_mpicxx} \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags}" \
    -DCMAKE_Fortran_COMPILER=%{scls_mpifort} \
    -DCMAKE_Fortran_FLAGS="%{scls_fcflags} %{scls_oflags}" \
    -DMPIEXEC_EXECUTABLE=%{scls_mpiexec} \
%if "%{scls_libs}" == "static"
	-DBUILD_SHARED_LIBS=OFF \
%else
	-DBUILD_STATIC_LIBS=OFF \
%if "%{scls_compiler}" == "intel"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
%endif
	-DNLOPT_CXX=ON \
	-DNLOPT_FORTRAN=ON \
	-DNLOPT_GUILE=OFF \
	-DNLOPT_MATLAB=OFF \
	-DNLOPT_OCTAVE=OFF \
	-DNLOPT_PYTHON=OFF \
	-DNLOPT_SWIG=OFF \
%endif
	-DNLOPT_TESTS=ON \
    ..
%make_build

%check
cd build
%make_build test

%install
cd build
%make_install

%files
%{scls_prefix}/include/nlopt.*
%{scls_prefix}/lib/cmake/nlopt
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libnlopt.a
%else
%{scls_prefix}/lib/libnlopt.so
%{scls_prefix}/lib/libnlopt.so.*
%endif
%{scls_prefix}/lib/pkgconfig/nlopt.pc
%{scls_prefix}/share/man/man3/nlopt.3
%{scls_prefix}/share/man/man3/nlopt_minimize.3
%{scls_prefix}/share/man/man3/nlopt_minimize_constrained.3


%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2.7.1-1
- Initial Package
