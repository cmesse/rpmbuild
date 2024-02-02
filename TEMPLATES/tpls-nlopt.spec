Name:           tpls-%{tpls_flavor}-2.7.1
Version:        2.7.1
Release:        1%{?dist}
Summary:        [brief description]

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

BuildRequires:  tpls-%{tpls_flavor}-cmake
BuildRequires:  ncurses-devel

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
mkdir build && cd build
CC=%{tpls_mpicc} \
CXX=%{tpls_mpicxx} \
FC=%{tpls_mpifort} \
%{tpls_cmake} \
	-DCMAKE_C_COMPILER=%{tpls_cc} \
    -DCMAKE_C_FLAGS="%{tpls_cflags}" \
    -DCMAKE_CXX_COMPILER=%{tpls_cxx} \
    -DCMAKE_CXX_FLAGS="%{tpls_cxxflags}" \
    -DCMAKE_Fortran_COMPILER=%{tpls_fc} \
    -DCMAKE_Fortran_FLAGS="%{tpls_fcflags}" \
%if "%{tpls_libs}" == "static"
	-DBUILD_SHARED_LIBS=OFF \
%else
	-DBUILD_STATIC_LIBS=OFF \
%if "%{tpls_compiler}" == "intel"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib" \
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
%{tpls_prefix}/include/nlopt.*
%{tpls_prefix}/lib/cmake/nlopt
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libnlopt.a
%else
%{tpls_prefix}/lib/libnlopt.so
%{tpls_prefix}/lib/libnlopt.so.*
%endif
%{tpls_prefix}/lib/pkgconfig/nlopt.pc
%{tpls_prefix}/share/man/man3/nlopt.3
%{tpls_prefix}/share/man/man3/nlopt_minimize.3
%{tpls_prefix}/share/man/man3/nlopt_minimize_constrained.3


%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2.7.1-1
- Initial Package
